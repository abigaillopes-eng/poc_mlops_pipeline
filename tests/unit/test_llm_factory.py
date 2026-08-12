"""Testes unitários da factory da camada LLM."""

import pytest

from calculator_api.src.llm.clients import (
    LocalMathLLMClient,
    OpenAICompatibleMathLLMClient,
    create_default_math_llm_client,
)
from calculator_api.src.llm.factory import create_math_question_service


def test_create_default_math_llm_client_should_return_local_by_default(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("LLM_PROVIDER", raising=False)

    client = create_default_math_llm_client()

    assert isinstance(client, LocalMathLLMClient)


def test_create_default_math_llm_client_should_return_local_when_provider_is_local(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("LLM_PROVIDER", "local")

    client = create_default_math_llm_client()

    assert isinstance(client, LocalMathLLMClient)


def test_create_default_math_llm_client_should_raise_error_without_api_key(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("LLM_PROVIDER", "openai-compatible")
    monkeypatch.delenv("LLM_API_KEY", raising=False)

    with pytest.raises(RuntimeError, match="LLM_PROVIDER=openai-compatible exige"):
        create_default_math_llm_client()


def test_create_default_math_llm_client_should_return_openai_compatible_client(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("LLM_PROVIDER", "openai-compatible")
    monkeypatch.setenv("LLM_API_KEY", "fake-api-key")
    monkeypatch.setenv("LLM_BASE_URL", "https://fake.example.com/v1")
    monkeypatch.setenv("LLM_MODEL", "fake-model")

    client = create_default_math_llm_client()

    assert isinstance(client, OpenAICompatibleMathLLMClient)


def test_create_math_question_service_should_return_service(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("LLM_PROVIDER", "local")

    service = create_math_question_service()

    response = service.answer_question("Quanto é 2 + 2?")

    assert response.numeric_result == 4
    assert response.provider == "local"