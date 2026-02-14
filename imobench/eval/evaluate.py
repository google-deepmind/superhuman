# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Benchmark evaluation runner for IMO-AnswerBench.

Loads model predictions and scores them against the ground truth answers.
"""

import csv
import json
from pathlib import Path
from typing import Any

from imobench.eval.answer_checker import check_answer

_BENCHMARKS_DIR = Path(__file__).resolve().parent.parent
_ANSWERBENCH_PATH = _BENCHMARKS_DIR / "answerbench_v2.csv"


def load_answerbench(
    path: str | Path | None = None,
) -> dict[str, dict[str, str]]:
    """Load IMO-AnswerBench ground truth.

    Args:
        path: Path to answerbench CSV. Defaults to answerbench_v2.csv.

    Returns:
        Dict mapping Problem ID to row data.
    """
    if path is None:
        path = _ANSWERBENCH_PATH
    path = Path(path)

    problems: dict[str, dict[str, str]] = {}
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            problems[row["Problem ID"]] = dict(row)
    return problems


def load_predictions(path: str | Path) -> dict[str, str]:
    """Load model predictions from CSV or JSONL.

    Expected CSV format:
        Problem ID,Model Answer
        imo-bench-algebra-001,3
        imo-bench-algebra-002,$\\log_2 a + 1$

    Expected JSONL format:
        {"problem_id": "imo-bench-algebra-001", "answer": "3"}

    Args:
        path: Path to predictions file.

    Returns:
        Dict mapping Problem ID to model answer string.
    """
    path = Path(path)
    predictions: dict[str, str] = {}

    if path.suffix == ".jsonl":
        with open(path, encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                obj = json.loads(line)
                pid = obj.get("problem_id", obj.get("Problem ID", ""))
                if not pid:
                    raise ValueError(
                        f"Missing problem ID in {path} line {line_num}"
                    )
                answer = obj.get("answer", obj.get("Model Answer", ""))
                predictions[pid] = str(answer)
    else:
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row_num, row in enumerate(reader, 2):
                pid = row.get("Problem ID", row.get("problem_id", ""))
                if not pid:
                    raise ValueError(
                        f"Missing problem ID in {path} row {row_num}"
                    )
                answer = row.get("Model Answer", row.get("answer", ""))
                predictions[pid] = str(answer)

    return predictions


def evaluate_predictions(
    predictions: dict[str, str],
    answerbench_path: str | Path | None = None,
) -> list[dict[str, Any]]:
    """Evaluate model predictions against IMO-AnswerBench.

    Args:
        predictions: Dict mapping Problem ID to model answer.
        answerbench_path: Path to answerbench CSV. Defaults to bundled v2.

    Returns:
        List of result dicts, one per problem, each containing:
            problem_id (str)
            category (str)
            subcategory (str)
            source (str)
            ground_truth (str)
            model_answer (str)
            correct (bool)
            method (str)
            details (str)
    """
    benchmark = load_answerbench(answerbench_path)
    results: list[dict[str, Any]] = []

    for pid, problem in benchmark.items():
        model_answer = predictions.get(pid, "")
        ground_truth = problem["Short Answer"]

        if not model_answer:
            result = {
                "correct": False,
                "method": "missing",
                "details": "No prediction provided",
            }
        else:
            result = check_answer(model_answer, ground_truth)

        results.append(
            {
                "problem_id": pid,
                "category": problem.get("Category", ""),
                "subcategory": problem.get("Subcategory", ""),
                "source": problem.get("Source", ""),
                "ground_truth": ground_truth,
                "model_answer": model_answer,
                **result,
            }
        )

    return results
