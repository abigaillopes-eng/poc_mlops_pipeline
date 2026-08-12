"""Schemas da camada de perguntas matemáticas com LLM."""

from pydantic import BaseModel, Field


class MathQuestionRequest(BaseModel):
    """Payload recebido pela API para perguntas matemáticas."""

    question: str = Field(
        min_length=1,
        description="Pergunta matemática feita pelo usuário.",
        examples=["Quanto é 2 + 2?"],
    )


class MathAnswerResponse(BaseModel):
    """Resposta retornada pela API para perguntas matemáticas."""

    question: str
    answer: str
    numeric_result: float | None
    provider: str
    model: str
    confidence: float


class MathLLMResult(BaseModel):
    """Resultado interno retornado por um client LLM."""

    question: str
    answer: str
    numeric_result: float | None
    provider: str
    model: str
    confidence: float
