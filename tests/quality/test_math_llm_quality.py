"""Testes de qualidade da camada LLM usando dataset de ouro."""

import json
from pathlib import Path
from typing import Any

import pytest

from calculator_api.src.llm.clients import LocalMathLLMClient
from calculator_api.src.llm.service import MathQuestionService

GOLDEN_DATASET_PATH = Path("data/golden_math_qa.jsonl")


def load_golden_dataset() -> list[dict[str, Any]]:
    """Carrega o dataset de ouro em formato JSONL."""
    records: list[dict[str, Any]] = []

    with GOLDEN_DATASET_PATH.open("r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                records.append(json.loads(line))

    return records


@pytest.mark.quality
@pytest.mark.parametrize("golden_case", load_golden_dataset())
def test_math_llm_quality_against_golden_dataset(
    golden_case: dict[str, Any],
) -> None:
    service = MathQuestionService(llm_client=LocalMathLLMClient())

    response = service.answer_question(str(golden_case["question"]))

    expected = float(golden_case["expected_numeric_result"])
    tolerance = float(golden_case["tolerance"])

    assert response.numeric_result is not None, (
        f"Caso {golden_case['id']} não retornou resultado numérico."
    )

    assert abs(response.numeric_result - expected) <= tolerance, (
        f"Caso {golden_case['id']} falhou. "
        f"Esperado={expected}, obtido={response.numeric_result}"
    )