"""Testes de integração da API."""

from fastapi.testclient import TestClient

from calculator_api.src.main import app

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
