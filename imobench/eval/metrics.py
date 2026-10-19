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

"""Metrics computation and reporting for IMO-AnswerBench evaluation."""

from collections import defaultdict
from typing import Any


def compute_metrics(results: list[dict[str, Any]]) -> dict[str, Any]:
    """Compute accuracy metrics from evaluation results.

    Args:
        results: List of result dicts from evaluate_predictions.

    Returns:
        Dict containing:
            overall: Overall accuracy and counts.
            by_category: Accuracy broken down by Category.
            by_subcategory: Accuracy broken down by Category/Subcategory.
            by_source: Accuracy broken down by Source.
            by_method: Count of answers resolved by each checking method.
    """
    total = len(results)
    correct = sum(1 for r in results if r["correct"])

    # By category
    cat_counts: dict[str, dict[str, int]] = defaultdict(
        lambda: {"total": 0, "correct": 0}
    )
    for r in results:
        cat = r.get("category", "Unknown")
        cat_counts[cat]["total"] += 1
        if r["correct"]:
            cat_counts[cat]["correct"] += 1

    # By subcategory
    subcat_counts: dict[str, dict[str, int]] = defaultdict(
        lambda: {"total": 0, "correct": 0}
    )
    for r in results:
        key = f"{r.get('category', 'Unknown')}/{r.get('subcategory', 'Unknown')}"
        subcat_counts[key]["total"] += 1
        if r["correct"]:
            subcat_counts[key]["correct"] += 1

    # By source
    source_counts: dict[str, dict[str, int]] = defaultdict(
        lambda: {"total": 0, "correct": 0}
    )
    for r in results:
        source = r.get("source", "Unknown")
        source_counts[source]["total"] += 1
        if r["correct"]:
            source_counts[source]["correct"] += 1

    # By method
    method_counts: dict[str, int] = defaultdict(int)
    for r in results:
        method_counts[r.get("method", "unknown")] += 1

    def _accuracy(counts: dict[str, int]) -> float:
        if counts["total"] == 0:
            return 0.0
        return counts["correct"] / counts["total"]

    return {
        "overall": {
            "total": total,
            "correct": correct,
            "accuracy": correct / total if total > 0 else 0.0,
        },
        "by_category": {
            cat: {**counts, "accuracy": _accuracy(counts)}
            for cat, counts in sorted(cat_counts.items())
        },
        "by_subcategory": {
            key: {**counts, "accuracy": _accuracy(counts)}
            for key, counts in sorted(subcat_counts.items())
        },
        "by_source": {
            src: {**counts, "accuracy": _accuracy(counts)}
            for src, counts in sorted(source_counts.items())
        },
        "by_method": dict(sorted(method_counts.items())),
    }


def format_report(metrics: dict[str, Any]) -> str:
    """Format metrics into a human-readable report.

    Args:
        metrics: Output from compute_metrics.

    Returns:
        Formatted string report.
    """
    lines: list[str] = []

    overall = metrics["overall"]
    lines.append("=" * 60)
    lines.append("IMO-AnswerBench Evaluation Report")
    lines.append("=" * 60)
    lines.append(
        f"Overall Accuracy: {overall['correct']}/{overall['total']} "
        f"({overall['accuracy']:.1%})"
    )
    lines.append("")

    lines.append("Accuracy by Category:")
    lines.append("-" * 40)
    for cat, data in metrics["by_category"].items():
        lines.append(
            f"  {cat:<25} {data['correct']:>3}/{data['total']:<3} "
            f"({data['accuracy']:.1%})"
        )
    lines.append("")

    lines.append("Accuracy by Subcategory:")
    lines.append("-" * 40)
    for key, data in metrics["by_subcategory"].items():
        lines.append(
            f"  {key:<35} {data['correct']:>3}/{data['total']:<3} "
            f"({data['accuracy']:.1%})"
        )
    lines.append("")

    lines.append("Checking Methods Used:")
    lines.append("-" * 40)
    for method, count in metrics["by_method"].items():
        lines.append(f"  {method:<25} {count:>4}")
    lines.append("")

    return "\n".join(lines)
