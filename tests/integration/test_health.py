"""Testes de integração da API FastAPI."""

from fastapi.testclient import TestClient

from meu_projeto.main import app

client = TestClient(app)


def test_health_check_should_return_ok() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_sum_endpoint_should_return_sum_result() -> None:
    response = client.post(
        "/sum",
        json={
            "first_number": 10,
            "second_number": 7,
        },
    )

    assert response.status_code == 200
    assert response.json() == {"result": 17}
