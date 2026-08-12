"""Testes unitários do client local de matemática."""

from calculator_api.src.llm.clients import LocalMathLLMClient


def test_local_client_should_answer_simple_sum() -> None:
    client = LocalMathLLMClient()

    result = client.answer_math_question("Quanto é 2 + 2?")

    assert result.numeric_result == 4
    assert "4" in result.answer
    assert result.provider == "local"


def test_local_client_should_answer_multiplication_in_portuguese() -> None:
    client = LocalMathLLMClient()

    result = client.answer_math_question("Quanto é 6 vezes 7?")

    assert result.numeric_result == 42


def test_local_client_should_answer_division_in_portuguese() -> None:
    client = LocalMathLLMClient()

    result = client.answer_math_question("Quanto é 20 dividido por 4?")

    assert result.numeric_result == 5


def test_local_client_should_answer_square_root() -> None:
    client = LocalMathLLMClient()

    result = client.answer_math_question("Qual é a raiz quadrada de 81?")

    assert result.numeric_result == 9


def test_local_client_should_answer_percentage() -> None:
    client = LocalMathLLMClient()

    result = client.answer_math_question("Quanto é 10% de 200?")

    assert result.numeric_result == 20


def test_local_client_should_return_none_when_question_is_not_supported() -> None:
    client = LocalMathLLMClient()

    result = client.answer_math_question("Explique a história da matemática.")

    assert result.numeric_result is None
    assert result.confidence == 0.2