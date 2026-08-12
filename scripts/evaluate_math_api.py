"""Avaliação da API matemática via HTTP usando dataset de ouro."""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = PROJECT_ROOT / "data" / "golden_math_qa.jsonl"
REPORT_PATH = PROJECT_ROOT / "llm_api_quality_report.json"

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
MINIMUM_REQUIRED_ACCURACY = float(os.getenv("MINIMUM_REQUIRED_ACCURACY", "1.0"))


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


def post_json(path: str, payload: dict[str, Any]) -> dict[str, Any]:
    """Envia uma requisição POST JSON para a API."""
    url = f"{API_BASE_URL}{path}"

    request = urllib.request.Request(
        url=url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
        },
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=10) as response:
        response_body = response.read().decode("utf-8")
        return json.loads(response_body)


def wait_for_health() -> None:
    """Aguarda a API responder no endpoint /health."""
    health_url = f"{API_BASE_URL}/health"

    for attempt in range(1, 31):
        try:
            with urllib.request.urlopen(health_url, timeout=5) as response:
                if response.status == 200:
                    print("API respondeu no /health.")
                    return
        except urllib.error.URLError as exc:
            print(f"Tentativa {attempt}/30: API ainda indisponível: {exc}")

        time.sleep(2)

    raise RuntimeError("API não respondeu no /health após 60 segundos.")


def main() -> None:
    """Executa avaliação contra a API Dockerizada."""
    wait_for_health()

    dataset = load_dataset()

    results: list[dict[str, Any]] = []
    passed = 0

    for case in dataset:
        api_response = post_json(
            path="/ask-math",
            payload={
                "question": case["question"],
            },
        )

        expected = float(case["expected_numeric_result"])
        tolerance = float(case["tolerance"])
        actual_raw = api_response.get("numeric_result")

        actual = float(actual_raw) if actual_raw is not None else None
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
                "provider": api_response.get("provider"),
                "model": api_response.get("model"),
                "answer": api_response.get("answer"),
            }
        )

    total = len(dataset)
    accuracy = passed / total if total else 0.0

    report = {
        "api_base_url": API_BASE_URL,
        "total": total,
        "passed": passed,
        "failed": total - passed,
        "accuracy": accuracy,
        "minimum_required_accuracy": MINIMUM_REQUIRED_ACCURACY,
        "status": "passed" if accuracy >= MINIMUM_REQUIRED_ACCURACY else "failed",
        "results": results,
    }

    REPORT_PATH.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(json.dumps(report, ensure_ascii=False, indent=2))

    if accuracy < MINIMUM_REQUIRED_ACCURACY:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
