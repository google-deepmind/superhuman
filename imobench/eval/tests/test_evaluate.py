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

"""Tests for the benchmark evaluation runner."""

import csv
import json
from pathlib import Path

import pytest

from imobench.eval.evaluate import (
    evaluate_predictions,
    load_predictions,
)


@pytest.fixture
def sample_answerbench(tmp_path: Path) -> Path:
    """Create a minimal answerbench CSV for testing."""
    path = tmp_path / "answerbench.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["Problem ID", "Problem", "Short Answer", "Category", "Subcategory", "Source"]
        )
        writer.writerow(["p-001", "What is 1+1?", "2", "Algebra", "Operation", "Test"])
        writer.writerow(
            ["p-002", "Simplify.", "$\\frac{1}{2}$", "Algebra", "Equation", "Test"]
        )
        writer.writerow(
            ["p-003", "Find all x.", "1, 2, 3", "Combinatorics", "Other", "Test"]
        )
    return path


@pytest.fixture
def sample_predictions_csv(tmp_path: Path) -> Path:
    """Create a sample predictions CSV."""
    path = tmp_path / "predictions.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Problem ID", "Model Answer"])
        writer.writerow(["p-001", "2"])
        writer.writerow(["p-002", "0.5"])
        writer.writerow(["p-003", "2, 1, 3"])
    return path


@pytest.fixture
def sample_predictions_jsonl(tmp_path: Path) -> Path:
    """Create a sample predictions JSONL."""
    path = tmp_path / "predictions.jsonl"
    with open(path, "w", encoding="utf-8") as f:
        for pid, answer in [("p-001", "2"), ("p-002", "0.5"), ("p-003", "2, 1, 3")]:
            f.write(json.dumps({"problem_id": pid, "answer": answer}) + "\n")
    return path


class TestLoadPredictions:
    def test_load_csv(self, sample_predictions_csv: Path):
        preds = load_predictions(sample_predictions_csv)
        assert preds["p-001"] == "2"
        assert preds["p-002"] == "0.5"
        assert len(preds) == 3

    def test_load_jsonl(self, sample_predictions_jsonl: Path):
        preds = load_predictions(sample_predictions_jsonl)
        assert preds["p-001"] == "2"
        assert preds["p-002"] == "0.5"
        assert len(preds) == 3


class TestEvaluatePredictions:
    def test_all_correct(
        self, sample_predictions_csv: Path, sample_answerbench: Path
    ):
        preds = load_predictions(sample_predictions_csv)
        results = evaluate_predictions(preds, sample_answerbench)
        assert len(results) == 3
        assert all(r["correct"] for r in results)

    def test_missing_prediction(self, sample_answerbench: Path):
        preds = {"p-001": "2"}  # Missing p-002, p-003
        results = evaluate_predictions(preds, sample_answerbench)
        correct_count = sum(1 for r in results if r["correct"])
        assert correct_count == 1
        missing = [r for r in results if r["method"] == "missing"]
        assert len(missing) == 2

    def test_empty_problem_id_raises(self, tmp_path: Path):
        path = tmp_path / "bad.csv"
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Problem ID", "Model Answer"])
            writer.writerow(["", "42"])
        with pytest.raises(ValueError, match="Missing problem ID"):
            load_predictions(path)

    def test_result_structure(
        self, sample_predictions_csv: Path, sample_answerbench: Path
    ):
        preds = load_predictions(sample_predictions_csv)
        results = evaluate_predictions(preds, sample_answerbench)
        for r in results:
            assert "problem_id" in r
            assert "category" in r
            assert "subcategory" in r
            assert "ground_truth" in r
            assert "model_answer" in r
            assert "correct" in r
            assert "method" in r
