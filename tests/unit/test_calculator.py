"""Testes unitários do módulo calculator."""

import pytest

from meu_projeto.calculator import divide_numbers, sum_numbers


def test_sum_numbers_should_return_sum() -> None:
    result = sum_numbers(first_number=10, second_number=5)

    assert result == 15


def test_sum_numbers_should_work_with_negative_values() -> None:
    result = sum_numbers(first_number=-10, second_number=5)

    assert result == -5


def test_divide_numbers_should_return_division_result() -> None:
    result = divide_numbers(dividend=10, divisor=2)

    assert result == 5


def test_divide_numbers_should_raise_error_when_divisor_is_zero() -> None:
    with pytest.raises(ValueError, match="O divisor não pode ser zero."):
        divide_numbers(dividend=10, divisor=0)
