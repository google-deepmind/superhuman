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

"""Tests for the metrics computation module."""

from imobench.eval.metrics import compute_metrics, format_report


SAMPLE_RESULTS = [
    {
        "problem_id": "p-001",
        "category": "Algebra",
        "subcategory": "Operation",
        "source": "Test",
        "ground_truth": "2",
        "model_answer": "2",
        "correct": True,
        "method": "exact_match",
        "details": "",
    },
    {
        "problem_id": "p-002",
        "category": "Algebra",
        "subcategory": "Equation",
        "source": "Test",
        "ground_truth": "$\\frac{1}{2}$",
        "model_answer": "0.5",
        "correct": True,
        "method": "sympy",
        "details": "",
    },
    {
        "problem_id": "p-003",
        "category": "Combinatorics",
        "subcategory": "Other",
        "source": "Test",
        "ground_truth": "5",
        "model_answer": "3",
        "correct": False,
        "method": "numeric",
        "details": "Expected 5, got 3",
    },
]


class TestComputeMetrics:
    def test_overall_accuracy(self):
        metrics = compute_metrics(SAMPLE_RESULTS)
        assert metrics["overall"]["total"] == 3
        assert metrics["overall"]["correct"] == 2
        assert abs(metrics["overall"]["accuracy"] - 2 / 3) < 1e-9

    def test_by_category(self):
        metrics = compute_metrics(SAMPLE_RESULTS)
        assert "Algebra" in metrics["by_category"]
        assert metrics["by_category"]["Algebra"]["total"] == 2
        assert metrics["by_category"]["Algebra"]["correct"] == 2
        assert "Combinatorics" in metrics["by_category"]
        assert metrics["by_category"]["Combinatorics"]["correct"] == 0

    def test_by_subcategory(self):
        metrics = compute_metrics(SAMPLE_RESULTS)
        assert "Algebra/Operation" in metrics["by_subcategory"]
        assert "Algebra/Equation" in metrics["by_subcategory"]

    def test_by_method(self):
        metrics = compute_metrics(SAMPLE_RESULTS)
        assert metrics["by_method"]["exact_match"] == 1
        assert metrics["by_method"]["sympy"] == 1
        assert metrics["by_method"]["numeric"] == 1

    def test_empty_results(self):
        metrics = compute_metrics([])
        assert metrics["overall"]["total"] == 0
        assert metrics["overall"]["accuracy"] == 0.0


class TestFormatReport:
    def test_report_contains_accuracy(self):
        metrics = compute_metrics(SAMPLE_RESULTS)
        report = format_report(metrics)
        assert "2/3" in report
        assert "66.7%" in report

    def test_report_contains_categories(self):
        metrics = compute_metrics(SAMPLE_RESULTS)
        report = format_report(metrics)
        assert "Algebra" in report
        assert "Combinatorics" in report
