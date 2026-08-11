"""Aplicação FastAPI da calculadora."""

from fastapi import FastAPI
from pydantic import BaseModel

from calculator_api.src.calculator import (
    divide_numbers,
    multiply_numbers,
    subtract_numbers,
    sum_numbers,
)

app = FastAPI(
    title="Calculator API",
    description="POC de calculadora com CI/CD usando GitHub Actions.",
    version="0.1.0",
)


class BinaryOperationRequest(BaseModel):
    """Payload para operações com dois números."""

    first_number: float
    second_number: float


class OperationResponse(BaseModel):
    """Resposta padrão das operações."""

    result: float


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
