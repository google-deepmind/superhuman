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

"""IMO-AnswerBench evaluation harness.

Provides tools to evaluate model outputs against IMO-AnswerBench ground truth
answers using mathematical equivalence checking.

Usage:
    from imobench.eval import check_answer, evaluate_predictions, compute_metrics

    result = check_answer("\\frac{1}{2}", "0.5")
    assert result["correct"] is True
"""

from imobench.eval.answer_checker import check_answer
from imobench.eval.evaluate import evaluate_predictions, load_predictions
from imobench.eval.metrics import compute_metrics, format_report

__all__ = [
    "check_answer",
    "evaluate_predictions",
    "load_predictions",
    "compute_metrics",
    "format_report",
]
