"""Serviço de perguntas matemáticas com camada LLM."""

from calculator_api.src.llm.clients import MathLLMClient
from calculator_api.src.llm.schemas import MathAnswerResponse


class MathQuestionService:
    """Serviço responsável por responder perguntas matemáticas."""

    def __init__(self, llm_client: MathLLMClient) -> None:
        self.llm_client = llm_client

    def answer_question(self, question: str) -> MathAnswerResponse:
        """Responde uma pergunta matemática."""
        normalized_question = question.strip()

        if not normalized_question:
            raise ValueError("A pergunta matemática não pode ser vazia.")

        llm_result = self.llm_client.answer_math_question(normalized_question)

        return MathAnswerResponse(
            question=llm_result.question,
            answer=llm_result.answer,
            numeric_result=llm_result.numeric_result,
            provider=llm_result.provider,
            model=llm_result.model,
            confidence=llm_result.confidence,
        )