"""Testes de qualidade da camada LLM usando dataset de ouro."""

import json
from pathlib import Path
from typing import Any

import pytest

from calculator_api.src.llm.clients import LocalMathLLMClient
from calculator_api.src.llm.service import MathQuestionService

PROJECT_ROOT = Path(__file__).resolve().parents[2]
GOLDEN_DATASET_PATH = PROJECT_ROOT / "data" / "golden_math_qa.jsonl"


def load_golden_dataset() -> list[dict[str, Any]]:
    """Carrega o dataset de ouro em formato JSONL."""
    if not GOLDEN_DATASET_PATH.exists():
        raise FileNotFoundError(f"Dataset de ouro não encontrado em: {GOLDEN_DATASET_PATH}")

    records: list[dict[str, Any]] = []

    with GOLDEN_DATASET_PATH.open("r", encoding="utf-8-sig") as file:
        for line_number, line in enumerate(file, start=1):
            clean_line = line.strip()

            if not clean_line:
                continue

            try:
                records.append(json.loads(clean_line))
            except json.JSONDecodeError as exc:
                raise ValueError(
                    "Linha inválida no dataset de ouro. "
                    f"Arquivo={GOLDEN_DATASET_PATH}, "
                    f"linha={line_number}, "
                    f"conteudo={clean_line!r}"
                ) from exc

    if not records:
        raise ValueError(f"Dataset de ouro está vazio: {GOLDEN_DATASET_PATH}")

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
        f"Caso {golden_case['id']} falhou. Esperado={expected}, obtido={response.numeric_result}"
    )
