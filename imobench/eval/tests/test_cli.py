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

"""Tests for the CLI module."""

import csv
import json
from pathlib import Path

import pytest

from imobench.eval.cli import main


@pytest.fixture
def sample_answerbench(tmp_path: Path) -> Path:
    path = tmp_path / "answerbench.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["Problem ID", "Problem", "Short Answer", "Category", "Subcategory", "Source"]
        )
        writer.writerow(["p-001", "Q1", "2", "Algebra", "Op", "Test"])
        writer.writerow(["p-002", "Q2", "5", "Algebra", "Eq", "Test"])
    return path


@pytest.fixture
def sample_predictions(tmp_path: Path) -> Path:
    path = tmp_path / "preds.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Problem ID", "Model Answer"])
        writer.writerow(["p-001", "2"])
        writer.writerow(["p-002", "3"])
    return path


class TestCli:
    def test_text_output(self, sample_predictions, sample_answerbench, capsys):
        main([str(sample_predictions), "--answerbench", str(sample_answerbench)])
        captured = capsys.readouterr()
        assert "Accuracy" in captured.out
        assert "1/2" in captured.out

    def test_json_output(self, sample_predictions, sample_answerbench, capsys):
        main([
            str(sample_predictions),
            "--answerbench", str(sample_answerbench),
            "--format", "json",
        ])
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert "metrics" in data
        assert "results" in data
        assert data["metrics"]["overall"]["total"] == 2

    def test_output_file(self, sample_predictions, sample_answerbench, tmp_path):
        out_path = tmp_path / "results.json"
        main([
            str(sample_predictions),
            "--answerbench", str(sample_answerbench),
            "--output", str(out_path),
        ])
        assert out_path.exists()
        data = json.loads(out_path.read_text(encoding="utf-8"))
        assert data["metrics"]["overall"]["total"] == 2

    def test_missing_file_exits(self):
        with pytest.raises(SystemExit) as exc_info:
            main(["nonexistent_file.csv"])
        assert exc_info.value.code == 1

    def test_empty_predictions_exits(self, tmp_path):
        path = tmp_path / "empty.csv"
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Problem ID", "Model Answer"])
        with pytest.raises(SystemExit) as exc_info:
            main([str(path)])
        assert exc_info.value.code == 1
