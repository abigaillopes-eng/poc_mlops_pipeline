"""Clients para a camada LLM de matemática."""

from __future__ import annotations

import ast
import math
import os
import re
from typing import Any, Protocol, cast

import httpx

from calculator_api.src.llm.prompt_builder import MathPromptBuilder
from calculator_api.src.llm.schemas import MathLLMResult


class MathLLMClient(Protocol):
    """Contrato para clients capazes de responder perguntas matemáticas."""

    def answer_math_question(self, question: str) -> MathLLMResult:
        """Responde uma pergunta matemática."""
        ...


class LocalMathLLMClient:
    """Client local determinístico para perguntas matemáticas.

    Este client não chama API externa. Ele existe para:
    - permitir testes unitários previsíveis;
    - permitir quality tests na pipeline;
    - simular a camada LLM durante a POC;
    - evitar dependência de secrets no CI/CD.
    """

    provider = "local"
    model = "deterministic-math-solver-v1"

    def answer_math_question(self, question: str) -> MathLLMResult:
        """Responde uma pergunta matemática usando avaliação segura local."""
        numeric_result = self._solve(question)

        if numeric_result is None:
            return MathLLMResult(
                question=question,
                answer=(
                    "Não consegui calcular essa pergunta com o resolvedor local. "
                    "Tente escrever a expressão com números e operadores."
                ),
                numeric_result=None,
                provider=self.provider,
                model=self.model,
                confidence=0.2,
            )

        formatted = self._format_number(numeric_result)

        return MathLLMResult(
            question=question,
            answer=f"O resultado é {formatted}.",
            numeric_result=numeric_result,
            provider=self.provider,
            model=self.model,
            confidence=1.0,
        )

    def _solve(self, question: str) -> float | None:
        normalized = self._normalize_question(question)

        square_root_result = self._try_square_root(normalized)
        if square_root_result is not None:
            return square_root_result

        percentage_result = self._try_percentage(normalized)
        if percentage_result is not None:
            return percentage_result

        expression = self._extract_expression(normalized)
        if expression is None:
            return None

        return self._safe_eval(expression)

    def _normalize_question(self, question: str) -> str:
        normalized = question.lower()

        replacements = {
            "quanto é": "",
            "quanto e": "",
            "calcule": "",
            "resolva": "",
            "qual é o resultado de": "",
            "qual e o resultado de": "",
            "mais": "+",
            "menos": "-",
            "vezes": "*",
            "multiplicado por": "*",
            "multiplicada por": "*",
            "dividido por": "/",
            "dividida por": "/",
            "sobre": "/",
            "elevado a": "**",
            "elevada a": "**",
            "x": "*",
            "×": "*",
            "÷": "/",
            "^": "**",
            ",": ".",
        }

        for old, new in replacements.items():
            normalized = normalized.replace(old, new)

        return normalized

    def _try_square_root(self, normalized_question: str) -> float | None:
        match = re.search(r"raiz quadrada de\s+(-?\d+(?:\.\d+)?)", normalized_question)

        if match is None:
            return None

        value = float(match.group(1))

        if value < 0:
            return None

        return math.sqrt(value)

    def _try_percentage(self, normalized_question: str) -> float | None:
        match = re.search(
            r"(-?\d+(?:\.\d+)?)\s*%\s*de\s*(-?\d+(?:\.\d+)?)",
            normalized_question,
        )

        if match is None:
            return None

        percentage = float(match.group(1))
        base_value = float(match.group(2))

        return (percentage / 100) * base_value

    def _extract_expression(self, normalized_question: str) -> str | None:
        allowed_chars = re.findall(r"[-+*/().0-9\s]+", normalized_question)
        expression = " ".join(part.strip() for part in allowed_chars if part.strip())

        if not expression:
            return None

        if not re.search(r"\d", expression):
            return None

        return expression

    def _safe_eval(self, expression: str) -> float | None:
        try:
            parsed = ast.parse(expression, mode="eval")
            result = self._eval_ast(parsed.body)
        except (SyntaxError, ValueError, ZeroDivisionError, TypeError):
            return None

        if abs(result) > 1_000_000_000_000:
            return None

        return float(result)

    def _eval_ast(self, node: ast.AST) -> float:
        if isinstance(node, ast.Constant):
            if isinstance(node.value, int | float):
                return float(node.value)

            raise ValueError("Constante inválida.")

        if isinstance(node, ast.UnaryOp):
            operand = self._eval_ast(node.operand)

            if isinstance(node.op, ast.UAdd):
                return operand

            if isinstance(node.op, ast.USub):
                return -operand

            raise ValueError("Operador unário inválido.")

        if isinstance(node, ast.BinOp):
            left = self._eval_ast(node.left)
            right = self._eval_ast(node.right)

            if isinstance(node.op, ast.Add):
                return left + right

            if isinstance(node.op, ast.Sub):
                return left - right

            if isinstance(node.op, ast.Mult):
                return left * right

            if isinstance(node.op, ast.Div):
                return left / right

            if isinstance(node.op, ast.Pow):
                return float(left**right)

            if isinstance(node.op, ast.Mod):
                return left % right

            raise ValueError("Operador binário inválido.")

        raise ValueError("Expressão inválida.")

    def _format_number(self, value: float) -> str:
        if value.is_integer():
            return str(int(value))

        return f"{value:.6f}".rstrip("0").rstrip(".")


class OpenAICompatibleMathLLMClient:
    """Client compatível com APIs estilo OpenAI Chat Completions.

    Este client é opcional. Ele só deve ser usado quando existirem as variáveis:

    - LLM_API_KEY
    - LLM_BASE_URL
    - LLM_MODEL

    Na pipeline, recomenda-se usar o provider local para evitar dependência de API externa.
    """

    provider = "openai-compatible"

    def __init__(
        self,
        api_key: str,
        base_url: str,
        model: str,
        timeout_seconds: float = 30.0,
    ) -> None:
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout_seconds = timeout_seconds
        self.prompt_builder = MathPromptBuilder()

    def answer_math_question(self, question: str) -> MathLLMResult:
        """Responde uma pergunta matemática usando um LLM externo."""
        system_prompt = self.prompt_builder.build_system_prompt()
        user_prompt = self.prompt_builder.build_user_prompt(question)

        payload: dict[str, Any] = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            "temperature": 0,
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        try:
            response = httpx.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=self.timeout_seconds,
            )
            response.raise_for_status()
        except httpx.HTTPError as exc:
            return MathLLMResult(
                question=question,
                answer=f"Falha ao consultar o LLM externo: {exc}",
                numeric_result=None,
                provider=self.provider,
                model=self.model,
                confidence=0.0,
            )

        response_data = cast(dict[str, Any], response.json())
        choices = cast(list[dict[str, Any]], response_data.get("choices", []))

        if not choices:
            return MathLLMResult(
                question=question,
                answer="O LLM não retornou resposta.",
                numeric_result=None,
                provider=self.provider,
                model=self.model,
                confidence=0.0,
            )

        message = cast(dict[str, Any], choices[0].get("message", {}))
        answer = str(message.get("content", "")).strip()

        return MathLLMResult(
            question=question,
            answer=answer,
            numeric_result=None,
            provider=self.provider,
            model=self.model,
            confidence=0.8,
        )


def create_default_math_llm_client() -> MathLLMClient:
    """Cria o client LLM padrão a partir de variáveis de ambiente."""
    provider = os.getenv("LLM_PROVIDER", "local").lower()

    if provider == "openai-compatible":
        api_key = os.getenv("LLM_API_KEY")
        base_url = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
        model = os.getenv("LLM_MODEL", "gpt-4o-mini")

        if not api_key:
            raise RuntimeError("LLM_PROVIDER=openai-compatible exige a variável LLM_API_KEY.")

        return OpenAICompatibleMathLLMClient(
            api_key=api_key,
            base_url=base_url,
            model=model,
        )

    return LocalMathLLMClient()
