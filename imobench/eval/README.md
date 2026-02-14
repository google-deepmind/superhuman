# IMO-AnswerBench Evaluation Harness

A Python tool for evaluating model outputs against the IMO-AnswerBench ground
truth answers using mathematical equivalence checking.

## Features

- **Math equivalence checking** via SymPy: correctly identifies equivalent
  mathematical expressions (e.g., `\frac{1}{2}` == `0.5`).
- **Multiple checking strategies**: exact match, numeric comparison, SymPy
  symbolic equivalence, multi-answer set matching, and normalized string
  comparison.
- **Detailed metrics**: accuracy breakdown by category, subcategory, and source.
- **CLI interface**: score predictions from the command line.
- **Flexible input**: accepts predictions as CSV or JSONL.

## Installation

```bash
pip install -r imobench/eval/requirements.txt
pip install pytest  # for running tests
```

## Usage

### Prepare predictions

Create a CSV file with your model's predictions:

```csv
Problem ID,Model Answer
imo-bench-algebra-001,3
imo-bench-algebra-002,$\lfloor \log_2 a \rfloor + 1$
```

Or a JSONL file:

```jsonl
{"problem_id": "imo-bench-algebra-001", "answer": "3"}
{"problem_id": "imo-bench-algebra-002", "answer": "$\\lfloor \\log_2 a \\rfloor + 1$"}
```

### Run evaluation

```bash
# Text report (default)
python -m imobench.eval.cli predictions.csv

# JSON output
python -m imobench.eval.cli predictions.csv --format json

# Save detailed results
python -m imobench.eval.cli predictions.csv --output results.json

# Use a custom answerbench path
python -m imobench.eval.cli predictions.csv --answerbench path/to/answerbench_v2.csv
```

### Python API

```python
from imobench.eval import check_answer, evaluate_predictions, compute_metrics, format_report
from imobench.eval.evaluate import load_predictions

# Check a single answer
result = check_answer(r"\frac{1}{2}", "0.5")
print(result)  # {'correct': True, 'method': 'sympy', 'details': ''}

# Evaluate a batch of predictions
predictions = load_predictions("predictions.csv")
results = evaluate_predictions(predictions)
metrics = compute_metrics(results)
print(format_report(metrics))
```

## Answer Checking Strategies

The checker tries strategies in this order and returns the first definitive
result:

| Strategy | Handles | Example |
|----------|---------|---------|
| Exact match | Identical normalized strings | `42` == `42` |
| Numeric | Plain numbers | `3.0` == `3` |
| Multi-answer | Comma-separated sets | `3, 1, 2` == `1, 2, 3` |
| SymPy | LaTeX math expressions | `\frac{1}{2}` == `0.5` |
| String normalized | Case/whitespace differences | `Algebra` == `algebra` |

## Running Tests

```bash
pytest imobench/eval/tests/ -v
```

## Limitations

- SymPy's LaTeX parser does not handle all mathematical notation (e.g., some
  piecewise functions, complex set-builder notation).
- Answers involving free variables or functions (e.g., `f(x) = 2x + c`) require
  structural matching that may not always succeed.
- For proof-based problems (IMO-ProofBench), use LLM-based grading with the
  autograder prompts instead.
