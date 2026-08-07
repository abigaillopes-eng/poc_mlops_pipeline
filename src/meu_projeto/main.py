"""Aplicação FastAPI principal."""

from fastapi import FastAPI
from pydantic import BaseModel

from meu_projeto.calculator import sum_numbers

app = FastAPI(
    title="Meu Projeto Python",
    description="API de exemplo para projeto Python com CI reutilizável.",
    version="0.1.0",
)


class SumRequest(BaseModel):
    """Payload para soma de dois números."""

    first_number: int
    second_number: int


class SumResponse(BaseModel):
    """Resposta da operação de soma."""

    result: int


@app.get("/health")
def health_check() -> dict[str, str]:
    """Endpoint de health check da aplicação."""
    return {"status": "ok"}


@app.post("/sum", response_model=SumResponse)
def sum_endpoint(payload: SumRequest) -> SumResponse:
    """Endpoint para somar dois números."""
    result = sum_numbers(
        first_number=payload.first_number,
        second_number=payload.second_number,
    )

    return SumResponse(result=result)
