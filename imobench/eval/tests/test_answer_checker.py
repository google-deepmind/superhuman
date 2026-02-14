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

"""Tests for the answer equivalence checker."""

import pytest

from imobench.eval.answer_checker import (
    _split_multi_answer,
    check_answer,
    normalize_latex,
)


class TestNormalizeLatex:
    def test_strips_dollar_signs(self):
        assert normalize_latex("$x+1$") == "x+1"

    def test_strips_double_dollar_signs(self):
        assert normalize_latex("$$x+1$$") == "x+1"

    def test_strips_trailing_period(self):
        assert normalize_latex("$x+1$.") == "x+1"

    def test_strips_whitespace(self):
        assert normalize_latex("  42  ") == "42"

    def test_combined(self):
        assert normalize_latex("  $\\frac{1}{2}$.  ") == "\\frac{1}{2}"


class TestSplitMultiAnswer:
    def test_single_answer(self):
        assert _split_multi_answer("42") == ["42"]

    def test_comma_separated(self):
        assert _split_multi_answer("1, 2, 3") == ["1", "2", "3"]

    def test_nested_braces(self):
        result = _split_multi_answer("f(x,y), g(x)")
        assert result == ["f(x,y)", "g(x)"]

    def test_empty_parts_filtered(self):
        result = _split_multi_answer("1,,2")
        assert result == ["1", "2"]


class TestCheckAnswer:
    # --- Exact match ---
    def test_exact_match(self):
        result = check_answer("42", "42")
        assert result["correct"] is True
        assert result["method"] == "exact_match"

    def test_exact_match_with_latex(self):
        result = check_answer("$\\frac{1}{2}$", "$\\frac{1}{2}$.")
        assert result["correct"] is True
        assert result["method"] == "exact_match"

    # --- Numeric ---
    def test_numeric_match(self):
        result = check_answer("3.0", "3")
        assert result["correct"] is True
        assert result["method"] == "numeric"

    def test_numeric_mismatch(self):
        result = check_answer("4", "3")
        assert result["correct"] is False
        assert result["method"] == "numeric"

    def test_negative_numeric(self):
        result = check_answer("-768", "-768.0")
        assert result["correct"] is True

    # --- Multi-answer ---
    def test_multi_answer_match(self):
        result = check_answer("1, 2, 3", "1, 2, 3")
        assert result["correct"] is True

    def test_multi_answer_reordered(self):
        result = check_answer("3, 1, 2", "1, 2, 3")
        assert result["correct"] is True
        assert result["method"] == "multi_answer"

    def test_multi_answer_wrong_count(self):
        result = check_answer("1, 2", "1, 2, 3")
        assert result["correct"] is False

    # --- SymPy equivalence ---
    def test_sympy_fraction(self):
        result = check_answer("\\frac{1}{2}", "0.5")
        assert result["correct"] is True
        assert result["method"] == "sympy"

    def test_sympy_equivalent_expression(self):
        result = check_answer("2^{3}", "8")
        assert result["correct"] is True

    def test_sympy_mismatch(self):
        result = check_answer("\\frac{1}{3}", "\\frac{1}{2}")
        assert result["correct"] is False

    # --- String normalization ---
    def test_string_case_insensitive(self):
        result = check_answer("Algebra", "algebra")
        assert result["correct"] is True
        assert result["method"] == "string_normalized"

    # --- No match ---
    def test_no_match(self):
        result = check_answer("foo", "bar")
        assert result["correct"] is False
        assert result["method"] == "no_match"
