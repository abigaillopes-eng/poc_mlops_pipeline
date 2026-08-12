"""Avaliação da camada LLM matemática usando dataset de ouro."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from calculator_api.src.llm.clients import create_default_math_llm_client
from calculator_api.src.llm.service import MathQuestionService

DATASET_PATH = PROJECT_ROOT / "data" / "golden_math_qa.jsonl"
REPORT_PATH = PROJECT_ROOT / "llm_quality_report.json"


def load_dataset() -> list[dict[str, Any]]:
    """Carrega o dataset de ouro em formato JSONL."""
    records: list[dict[str, Any]] = []

    with DATASET_PATH.open("r", encoding="utf-8-sig") as file:
        for line_number, line in enumerate(file, start=1):
            clean_line = line.strip()

            if not clean_line:
                continue

            try:
                records.append(json.loads(clean_line))
            except json.JSONDecodeError as exc:
                raise ValueError(
                    "Linha inválida no dataset de ouro. "
                    f"Arquivo={DATASET_PATH}, "
                    f"linha={line_number}, "
                    f"conteudo={clean_line!r}"
                ) from exc

    if not records:
        raise ValueError(f"Dataset de ouro está vazio: {DATASET_PATH}")

    return records


def main() -> None:
    """Executa a avaliação da camada LLM."""
    dataset = load_dataset()
    service = MathQuestionService(llm_client=create_default_math_llm_client())

    results: list[dict[str, Any]] = []
    passed = 0

    for case in dataset:
        response = service.answer_question(str(case["question"]))

        expected = float(case["expected_numeric_result"])
        tolerance = float(case["tolerance"])
        actual = response.numeric_result

        is_passed = actual is not None and abs(actual - expected) <= tolerance

        if is_passed:
            passed += 1

        results.append(
            {
                "id": case["id"],
                "question": case["question"],
                "category": case.get("category"),
                "difficulty": case.get("difficulty"),
                "expected_numeric_result": expected,
                "actual_numeric_result": actual,
                "passed": is_passed,
                "provider": response.provider,
                "model": response.model,
                "answer": response.answer,
            }
        )

    total = len(dataset)
    accuracy = passed / total if total else 0.0

    report = {
        "total": total,
        "passed": passed,
        "failed": total - passed,
        "accuracy": accuracy,
        "minimum_required_accuracy": 1.0,
        "status": "passed" if accuracy >= 1.0 else "failed",
        "results": results,
    }

    REPORT_PATH.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(json.dumps(report, ensure_ascii=False, indent=2))

    if accuracy < 1.0:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
