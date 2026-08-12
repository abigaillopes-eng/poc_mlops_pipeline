"""Testes de integração da API."""

from fastapi.testclient import TestClient

from calculator_api.src.llm.clients import LocalMathLLMClient
from calculator_api.src.llm.service import MathQuestionService
from calculator_api.src.main import app, get_math_question_service


def override_math_question_service() -> MathQuestionService:
    """Sobrescreve o serviço LLM para usar provider local nos testes."""
    return MathQuestionService(llm_client=LocalMathLLMClient())


app.dependency_overrides[get_math_question_service] = override_math_question_service

client = TestClient(app)


def test_health_check_should_return_ok() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_sum_endpoint_should_return_result() -> None:
    response = client.post(
        "/sum",
        json={
            "first_number": 10,
            "second_number": 5,
        },
    )

    assert response.status_code == 200
    assert response.json() == {"result": 15}


def test_subtract_endpoint_should_return_result() -> None:
    response = client.post(
        "/subtract",
        json={
            "first_number": 10,
            "second_number": 5,
        },
    )

    assert response.status_code == 200
    assert response.json() == {"result": 5}


def test_multiply_endpoint_should_return_result() -> None:
    response = client.post(
        "/multiply",
        json={
            "first_number": 10,
            "second_number": 5,
        },
    )

    assert response.status_code == 200
    assert response.json() == {"result": 50}


def test_divide_endpoint_should_return_result() -> None:
    response = client.post(
        "/divide",
        json={
            "first_number": 10,
            "second_number": 5,
        },
    )

    assert response.status_code == 200
    assert response.json() == {"result": 2}


def test_ask_math_endpoint_should_answer_question() -> None:
    response = client.post(
        "/ask-math",
        json={
            "question": "Quanto é 2 + 2?",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["question"] == "Quanto é 2 + 2?"
    assert body["numeric_result"] == 4
    assert body["provider"] == "local"
    assert "4" in body["answer"]
