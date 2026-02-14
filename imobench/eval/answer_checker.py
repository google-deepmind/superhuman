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

"""Mathematical answer equivalence checking for IMO-AnswerBench.

Supports numeric comparison, LaTeX expression parsing via SymPy, and
multi-answer (comma-separated) set matching.
"""

import math
import re
import threading
from typing import Any

from sympy import simplify
from sympy.parsing.latex import parse_latex

_SYMPY_TIMEOUT_SEC = 5


def normalize_latex(text: str) -> str:
    """Strip LaTeX delimiters, whitespace, and trailing punctuation."""
    text = text.strip()
    # Strip trailing punctuation before removing $ delimiters,
    # since periods often appear outside: "$x+1$."
    text = text.rstrip(".")
    text = text.strip()
    text = re.sub(r"^\$+|\$+$", "", text)
    text = text.strip()
    return text


def _looks_like_math(text: str) -> bool:
    """Heuristic check for LaTeX math notation."""
    return bool(re.search(r"[\\^_{}]", text))


def _split_multi_answer(text: str) -> list[str]:
    """Split comma-separated answers respecting nested braces and parens."""
    parts: list[str] = []
    depth = 0
    current: list[str] = []
    for ch in text:
        if ch in "({[":
            depth += 1
        elif ch in ")}]":
            depth = max(0, depth - 1)
        elif ch == "," and depth == 0:
            parts.append("".join(current).strip())
            current = []
            continue
        current.append(ch)
    parts.append("".join(current).strip())
    return [p for p in parts if p]


def _try_parse_number(text: str) -> float | None:
    """Try to parse a normalized string as a finite number."""
    try:
        val = float(text)
        if math.isfinite(val):
            return val
        return None
    except ValueError:
        return None


def _run_with_timeout(fn, timeout_sec: int = _SYMPY_TIMEOUT_SEC) -> Any:
    """Run a callable with a timeout. Returns None on timeout or error."""
    result: list[Any] = [None]
    error: list[bool] = [False]

    def target():
        try:
            result[0] = fn()
        except Exception:
            error[0] = True

    thread = threading.Thread(target=target, daemon=True)
    thread.start()
    thread.join(timeout=timeout_sec)
    if thread.is_alive() or error[0]:
        return None
    return result[0]


def _try_parse_sympy(text: str) -> Any:
    """Try to parse a LaTeX string into a SymPy expression with timeout."""
    return _run_with_timeout(lambda: parse_latex(text))


def _expressions_equivalent(expr_a: Any, expr_b: Any) -> bool:
    """Check if two SymPy expressions are mathematically equivalent."""
    def _check():
        diff = simplify(expr_a - expr_b)
        if diff == 0:
            return True
        if hasattr(diff, "is_zero") and diff.is_zero:
            return True
        return False

    result = _run_with_timeout(_check)
    if result is True:
        return True

    def _check_equals():
        return bool(expr_a.equals(expr_b))

    result = _run_with_timeout(_check_equals)
    return result is True


def check_answer(
    model_answer: str, ground_truth: str, _depth: int = 0
) -> dict[str, Any]:
    """Check if a model answer matches the ground truth.

    Tries multiple strategies in order:
    1. Exact string match (after normalization)
    2. Numeric comparison
    3. Multi-answer set matching (comma-separated)
    4. Normalized string comparison (case/whitespace insensitive)
    5. SymPy mathematical equivalence (only for math-like expressions)

    Args:
        model_answer: The model's predicted answer (plain text or LaTeX).
        ground_truth: The ground truth answer from the benchmark.

    Returns:
        A dict with keys:
            correct (bool): Whether the answer is correct.
            method (str): Which strategy determined the result.
            details (str): Additional information about the comparison.
    """
    model_norm = normalize_latex(model_answer)
    truth_norm = normalize_latex(ground_truth)

    # 1. Exact string match
    if model_norm == truth_norm:
        return {"correct": True, "method": "exact_match", "details": ""}

    # 2. Numeric comparison
    model_num = _try_parse_number(model_norm)
    truth_num = _try_parse_number(truth_norm)
    if model_num is not None and truth_num is not None:
        if abs(model_num - truth_num) < 1e-9:
            return {"correct": True, "method": "numeric", "details": ""}
        return {
            "correct": False,
            "method": "numeric",
            "details": f"Expected {truth_num}, got {model_num}",
        }

    # 3. Multi-answer (comma-separated sets)
    truth_parts = _split_multi_answer(truth_norm)
    if len(truth_parts) > 1 and _depth < 2:
        model_parts = _split_multi_answer(model_norm)
        if len(model_parts) != len(truth_parts):
            return {
                "correct": False,
                "method": "multi_answer",
                "details": (
                    f"Expected {len(truth_parts)} answers, "
                    f"got {len(model_parts)}"
                ),
            }
        matched: set[int] = set()
        for mp in model_parts:
            for i, tp in enumerate(truth_parts):
                if i not in matched:
                    sub_result = check_answer(mp, tp, _depth=_depth + 1)
                    if sub_result["correct"]:
                        matched.add(i)
                        break
        if len(matched) == len(truth_parts):
            return {
                "correct": True,
                "method": "multi_answer",
                "details": "All parts matched",
            }
        return {
            "correct": False,
            "method": "multi_answer",
            "details": f"Matched {len(matched)}/{len(truth_parts)} parts",
        }

    # 4. Normalized string comparison
    model_clean = re.sub(r"\s+", " ", model_norm.lower())
    truth_clean = re.sub(r"\s+", " ", truth_norm.lower())
    if model_clean == truth_clean:
        return {"correct": True, "method": "string_normalized", "details": ""}

    # 5. SymPy expression comparison (only for math-like expressions)
    if _looks_like_math(model_norm) or _looks_like_math(truth_norm):
        model_expr = _try_parse_sympy(model_norm)
        truth_expr = _try_parse_sympy(truth_norm)
        if model_expr is not None and truth_expr is not None:
            if _expressions_equivalent(model_expr, truth_expr):
                return {"correct": True, "method": "sympy", "details": ""}
            return {
                "correct": False,
                "method": "sympy",
                "details": "Expressions not equivalent",
            }

    return {
        "correct": False,
        "method": "no_match",
        "details": "Could not determine equivalence",
    }
