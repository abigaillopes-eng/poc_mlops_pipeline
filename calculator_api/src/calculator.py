"""Regras de negócio da calculadora."""


def sum_numbers(first_number: int, second_number: int) -> int:
    """Soma dois números inteiros."""
    return first_number + second_number


def subtract_numbers(first_number: int, second_number: int) -> int:
    """Subtrai dois números inteiros."""
    return first_number - second_number


def multiply_numbers(first_number: int, second_number: int) -> int:
    """Multiplica dois números inteiros."""
    return first_number * second_number


def divide_numbers(first_number: float, second_number: float) -> float:
    """Divide dois números.

    Raises:
        ValueError: Quando o divisor for zero.
    """
    if second_number == 0:
        raise ValueError("Não é possível dividir por zero.")

    return first_number / second_number
