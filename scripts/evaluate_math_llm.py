"""Avaliação da camada LLM matemática usando dataset de ouro."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from calculator_api.src.llm.clients import create_default_math_llm_client
from calculator_api.src.llm.service import MathQuestionService

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = PROJECT_ROOT / "data" / "golden_math_qa.jsonl"
REPORT_PATH = PROJECT_ROOT / "llm_quality_report.json"


def load_dataset() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []

    with DATASET_PATH.open("r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                records.append(json.loads(line))

    return records


def main() -> None:
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
