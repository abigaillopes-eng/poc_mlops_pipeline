"""Testes unitários do client OpenAI-compatible."""

from typing import Any

import httpx
import pytest

from calculator_api.src.llm.clients import OpenAICompatibleMathLLMClient


class FakeResponse:
    """Resposta fake para simular httpx.Response."""

    def __init__(self, payload: dict[str, Any]) -> None:
        self.payload = payload

    def raise_for_status(self) -> None:
        """Simula resposta HTTP sem erro."""

    def json(self) -> dict[str, Any]:
        """Retorna payload mockado."""
        return self.payload


def test_openai_compatible_client_should_return_answer(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_post(
        url: str,
        headers: dict[str, str],
        json: dict[str, Any],
        timeout: float,
    ) -> FakeResponse:
        assert url == "https://fake.example.com/v1/chat/completions"
        assert headers["Authorization"] == "Bearer fake-api-key"
        assert json["model"] == "fake-model"
        assert timeout == 30.0

        return FakeResponse({"choices": [{"message": {"content": "O resultado é 4."}}]})

    monkeypatch.setattr(httpx, "post", fake_post)

    client = OpenAICompatibleMathLLMClient(
        api_key="fake-api-key",
        base_url="https://fake.example.com/v1",
        model="fake-model",
    )

    result = client.answer_math_question("Quanto é 2 + 2?")

    assert result.answer == "O resultado é 4."
    assert result.numeric_result is None
    assert result.provider == "openai-compatible"
    assert result.model == "fake-model"
    assert result.confidence == 0.8


def test_openai_compatible_client_should_handle_empty_choices(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_post(
        url: str,
        headers: dict[str, str],
        json: dict[str, Any],
        timeout: float,
    ) -> FakeResponse:
        return FakeResponse({"choices": []})

    monkeypatch.setattr(httpx, "post", fake_post)

    client = OpenAICompatibleMathLLMClient(
        api_key="fake-api-key",
        base_url="https://fake.example.com/v1",
        model="fake-model",
    )

    result = client.answer_math_question("Quanto é 2 + 2?")

    assert result.answer == "O LLM não retornou resposta."
    assert result.numeric_result is None
    assert result.provider == "openai-compatible"
    assert result.confidence == 0.0
