"""Módulo de exemplo com regra de negócio simples."""


def sum_numbers(first_number: int, second_number: int) -> int:
    """Soma dois números inteiros.

    Args:
        first_number: Primeiro número.
        second_number: Segundo número.

    Returns:
        Resultado da soma.
    """
    return first_number + second_number


def divide_numbers(dividend: float, divisor: float) -> float:
    """Divide dois números.

    Args:
        dividend: Número que será dividido.
        divisor: Número divisor.

    Raises:
        ValueError: Quando o divisor for zero.

    Returns:
        Resultado da divisão.
    """
    if divisor == 0:
        raise ValueError("O divisor não pode ser zero.")

    return dividend / divisor
