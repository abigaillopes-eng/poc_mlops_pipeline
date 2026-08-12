"""Testes unitários do serviço de perguntas matemáticas."""

import pytest

from calculator_api.src.llm.clients import LocalMathLLMClient
from calculator_api.src.llm.service import MathQuestionService


def test_math_question_service_should_answer_question() -> None:
    service = MathQuestionService(llm_client=LocalMathLLMClient())

    response = service.answer_question("Quanto é 5 + 5?")

    assert response.numeric_result == 10
    assert response.provider == "local"
    assert response.model == "deterministic-math-solver-v1"


def test_math_question_service_should_raise_error_when_question_is_empty() -> None:
    service = MathQuestionService(llm_client=LocalMathLLMClient())

    with pytest.raises(ValueError, match="A pergunta matemática não pode ser vazia."):
        service.answer_question("   ")