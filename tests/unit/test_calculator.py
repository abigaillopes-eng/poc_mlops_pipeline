"""Testes unitários da calculadora."""

import pytest

from calculator_api.src.calculator import (
    divide_numbers,
    multiply_numbers,
    subtract_numbers,
    sum_numbers,
)


def test_sum_numbers_should_return_sum() -> None:
    result = sum_numbers(10, 5)

    assert result == 15


def test_subtract_numbers_should_return_difference() -> None:
    result = subtract_numbers(10, 5)

    assert result == 5


def test_multiply_numbers_should_return_product() -> None:
    result = multiply_numbers(10, 5)

    assert result == 50


def test_divide_numbers_should_return_division() -> None:
    result = divide_numbers(10, 5)

    assert result == 2


def test_divide_numbers_should_raise_error_when_dividing_by_zero() -> None:
    with pytest.raises(ValueError, match="Não é possível dividir por zero."):
        divide_numbers(10, 0)
