"""Testes opcionais da camada LLM usando provider externo real."""

import os

import pytest

from calculator_api.src.llm.clients import create_default_math_llm_client
from calculator_api.src.llm.service import MathQuestionService


@pytest.mark.llm_external
def test_external_llm_should_answer_math_question() -> None:
    """Valida se o provider externo responde uma pergunta matemática simples.

    Este teste não deve rodar em pytest comum.
    Ele só roda quando RUN_EXTERNAL_LLM_TESTS=true.
    """
    if os.getenv("RUN_EXTERNAL_LLM_TESTS") != "true":
        pytest.skip("Teste externo ignorado. Defina RUN_EXTERNAL_LLM_TESTS=true para executar.")

    if os.getenv("LLM_PROVIDER") != "openai-compatible":
        pytest.skip("LLM_PROVIDER não é openai-compatible.")

    if not os.getenv("LLM_API_KEY"):
        pytest.skip("LLM_API_KEY não foi configurada.")

    service = MathQuestionService(llm_client=create_default_math_llm_client())

    response = service.answer_question("Quanto é 2 + 2?")

    assert response.answer
    assert response.provider == "openai-compatible"
