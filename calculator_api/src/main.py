"""Aplicação FastAPI da calculadora."""

from fastapi import Depends, FastAPI
from pydantic import BaseModel

from calculator_api.src.calculator import (
    divide_numbers,
    multiply_numbers,
    subtract_numbers,
    sum_numbers,
)
from calculator_api.src.llm.factory import create_math_question_service
from calculator_api.src.llm.schemas import MathAnswerResponse, MathQuestionRequest
from calculator_api.src.llm.service import MathQuestionService

app = FastAPI(
    title="Calculator API",
    description="POC de calculadora com CI/CD e camada LLM.",
    version="0.2.0",
)


class BinaryOperationRequest(BaseModel):
    """Payload para operações com dois números."""

    first_number: float
    second_number: float


class OperationResponse(BaseModel):
    """Resposta padrão das operações."""

    result: float


def get_math_question_service() -> MathQuestionService:
    """Cria o serviço de perguntas matemáticas.

    Esta função existe para permitir sobrescrita nos testes.
    """
    return create_math_question_service()


@app.get("/health")
def health_check() -> dict[str, str]:
    """Verifica se a API está saudável."""
    return {"status": "ok"}


@app.post("/sum", response_model=OperationResponse)
def sum_endpoint(payload: BinaryOperationRequest) -> OperationResponse:
    """Soma dois números."""
    result = sum_numbers(
        int(payload.first_number),
        int(payload.second_number),
    )

    return OperationResponse(result=result)


@app.post("/subtract", response_model=OperationResponse)
def subtract_endpoint(payload: BinaryOperationRequest) -> OperationResponse:
    """Subtrai dois números."""
    result = subtract_numbers(
        int(payload.first_number),
        int(payload.second_number),
    )

    return OperationResponse(result=result)


@app.post("/multiply", response_model=OperationResponse)
def multiply_endpoint(payload: BinaryOperationRequest) -> OperationResponse:
    """Multiplica dois números."""
    result = multiply_numbers(
        int(payload.first_number),
        int(payload.second_number),
    )

    return OperationResponse(result=result)


@app.post("/divide", response_model=OperationResponse)
def divide_endpoint(payload: BinaryOperationRequest) -> OperationResponse:
    """Divide dois números."""
    result = divide_numbers(
        payload.first_number,
        payload.second_number,
    )

    return OperationResponse(result=result)


@app.post("/ask-math", response_model=MathAnswerResponse)
def ask_math_question(
    payload: MathQuestionRequest,
    service: MathQuestionService = Depends(get_math_question_service),
) -> MathAnswerResponse:
    """Responde qualquer pergunta matemática usando a camada LLM."""
    return service.answer_question(payload.question)
