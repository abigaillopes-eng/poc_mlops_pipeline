"""Testes unitários do prompt builder."""

from calculator_api.src.llm.prompt_builder import MathPromptBuilder


def test_build_system_prompt_should_return_math_instruction() -> None:
    builder = MathPromptBuilder()

    prompt = builder.build_system_prompt()

    assert "assistente matemático" in prompt
    assert "resultado numérico" in prompt


def test_build_user_prompt_should_include_question() -> None:
    builder = MathPromptBuilder()

    prompt = builder.build_user_prompt("Quanto é 2 + 2?")

    assert "Resolva a seguinte pergunta matemática" in prompt
    assert "Quanto é 2 + 2?" in prompt