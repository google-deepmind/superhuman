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

"""Command-line interface for IMO-AnswerBench evaluation.

Usage:
    python -m imobench.eval.cli predictions.csv
    python -m imobench.eval.cli predictions.jsonl --output results.json
    python -m imobench.eval.cli predictions.csv --answerbench path/to/answerbench_v2.csv
"""

import argparse
import json
import sys

from imobench.eval.evaluate import evaluate_predictions, load_predictions
from imobench.eval.metrics import compute_metrics, format_report


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Evaluate model predictions against IMO-AnswerBench.",
    )
    parser.add_argument(
        "predictions",
        help="Path to predictions file (CSV or JSONL).",
    )
    parser.add_argument(
        "--answerbench",
        default=None,
        help="Path to answerbench CSV (defaults to bundled answerbench_v2.csv).",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Path to write detailed results as JSON.",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format for the report (default: text).",
    )

    args = parser.parse_args(argv)

    try:
        predictions = load_predictions(args.predictions)
    except FileNotFoundError:
        print(f"Error: File not found: {args.predictions}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if not predictions:
        print("Error: No predictions loaded.", file=sys.stderr)
        sys.exit(1)

    try:
        results = evaluate_predictions(predictions, args.answerbench)
    except FileNotFoundError:
        print(
            f"Error: Answerbench not found: {args.answerbench}",
            file=sys.stderr,
        )
        sys.exit(1)
    metrics = compute_metrics(results)

    if args.format == "json":
        output = {"metrics": metrics, "results": results}
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print(format_report(metrics))

    if args.output:
        output = {"metrics": metrics, "results": results}
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        print(f"\nDetailed results written to {args.output}")


if __name__ == "__main__":
    main()
