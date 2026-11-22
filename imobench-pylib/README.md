# IMO Bench Python Library

A Python library for loading and working with the **IMO Bench** mathematical reasoning benchmarks from Google DeepMind.

## Overview

IMO Bench is a suite of advanced benchmarks designed to evaluate robust mathematical reasoning in AI systems. This library provides a simple, type-safe interface for loading and working with the benchmark datasets.

### Datasets

- **IMO-AnswerBench**: 400 challenging short-answer problems
- **IMO-ProofBench**: 60 expert-vetted proof-based problems
- **IMO-GradingBench**: 1000 human gradings for automatic evaluation development

## Installation

### From Source

```bash
cd imobench-pylib
pip install -e .
```

### Development Installation

```bash
pip install -e ".[dev]"
```

## Quick Start

```python
from imobench import load_answerbench, load_proofbench, load_gradingbench

# Load all short-answer problems
problems = load_answerbench()
print(f"Loaded {len(problems)} problems")

# Filter by category
algebra_problems = load_answerbench(category="Algebra")
for problem in algebra_problems[:3]:
    print(f"{problem.problem_id}: {problem.subcategory}")

# Load proof-based problems
proof_problems = load_proofbench(level="IMO-easy")

# Load grading data (use lazy loading for efficiency)
for grading in load_gradingbench(min_points=8, lazy=True):
    print(f"Problem {grading.problem_id}: {grading.points}/10 points")
    break  # Process one at a time
```

## Usage Examples

### Basic Loading

```python
from imobench import load_answerbench

# Load all problems
problems = load_answerbench()

# Access problem fields
problem = problems[0]
print(problem.problem_id)      # "imo-bench-algebra-001"
print(problem.category)        # "Algebra"
print(problem.subcategory)     # "Operation"
print(problem.problem)         # LaTeX problem statement
print(problem.short_answer)    # Expected answer
print(problem.source)          # "IMO Shortlist 2021"
```

### Filtering

```python
# Filter by category
geometry_problems = load_answerbench(category="Geometry")

# Filter by source
imo_2021 = load_answerbench(source="IMO Shortlist 2021")

# Multiple filters
algebra_inequalities = load_answerbench(
    category="Algebra",
    subcategory="Inequality"
)
```

### Working with ProofBench

```python
from imobench import load_proofbench

# Load by difficulty level
easy_problems = load_proofbench(level="IMO-easy")

# Access detailed fields
problem = easy_problems[0]
print(problem.solution)            # Reference solution
print(problem.grading_guidelines)  # Grading criteria
```

### Efficient GradingBench Processing

```python
from imobench import load_gradingbench

# Load specific problem's gradings
gradings = load_gradingbench(problem_id="PB-Basic-001")

# Filter by score range
high_quality = load_gradingbench(min_points=8)

# Lazy loading for memory efficiency (recommended for large datasets)
for grading in load_gradingbench(lazy=True):
    # Process one at a time
    analyze_response(grading.response, grading.points)
```

### Custom Data Directory

```python
from imobench import IMOBenchLoader
from pathlib import Path

# Specify custom data location
loader = IMOBenchLoader(data_dir=Path("/path/to/imobench/data"))
problems = loader.load_answerbench()
```

### Type-Safe Access

All data types are immutable dataclasses with full type hints:

```python
from imobench.types import AnswerBenchProblem

problem: AnswerBenchProblem = problems[0]
# IDE will provide autocomplete and type checking
```

## Data Schema

### AnswerBenchProblem

| Field | Type | Description |
|-------|------|-------------|
| `problem_id` | `str` | Unique identifier (e.g., "imo-bench-algebra-001") |
| `problem` | `str` | Problem statement in LaTeX format |
| `short_answer` | `str` | Expected answer |
| `category` | `str` | Main category (Algebra, Combinatorics, Geometry, Number theory) |
| `subcategory` | `str` | Specific subcategory |
| `source` | `str` | Original source of the problem |

### ProofBenchProblem

| Field | Type | Description |
|-------|------|-------------|
| `problem_id` | `str` | Unique identifier (e.g., "PB-Basic-001") |
| `problem` | `str` | Problem statement |
| `solution` | `str` | Reference solution |
| `grading_guidelines` | `str` | Guidelines for partial credit |
| `category` | `str` | Main category |
| `level` | `str` | Difficulty level (IMO-easy, pre-IMO, etc.) |
| `short_answer` | `str` | Brief expected answer |
| `source` | `str` | Original source |

### GradingBenchEntry

| Field | Type | Description |
|-------|------|-------------|
| `grading_id` | `str` | Unique identifier (e.g., "GB-0001") |
| `problem_id` | `str` | Reference to problem |
| `problem` | `str` | Problem statement |
| `solution` | `str` | Reference solution |
| `grading_guidelines` | `str` | Grading criteria |
| `response` | `str` | The response being graded |
| `points` | `int` | Points awarded (0-10) |
| `reward` | `float` | Reward value |
| `problem_source` | `str` | Original source |

## API Reference

### Loading Functions

#### `load_answerbench(**kwargs) -> list[AnswerBenchProblem]`

Load IMO-AnswerBench dataset.

**Parameters:**
- `category` (Optional[str]): Filter by category
- `subcategory` (Optional[str]): Filter by subcategory
- `source` (Optional[str]): Filter by source
- `validate` (bool): Enable validation (default: True)

#### `load_proofbench(**kwargs) -> list[ProofBenchProblem]`

Load IMO-ProofBench dataset.

**Parameters:**
- `category` (Optional[str]): Filter by category
- `level` (Optional[str]): Filter by difficulty level
- `validate` (bool): Enable validation (default: True)

#### `load_gradingbench(**kwargs) -> list[GradingBenchEntry] | Iterator[GradingBenchEntry]`

Load IMO-GradingBench dataset.

**Parameters:**
- `problem_id` (Optional[str]): Filter by problem ID
- `min_points` (Optional[int]): Minimum points threshold
- `max_points` (Optional[int]): Maximum points threshold
- `validate` (bool): Enable validation (default: True)
- `lazy` (bool): Return iterator for memory efficiency (default: False)

### Class: IMOBenchLoader

Advanced loader with custom data directory support.

```python
loader = IMOBenchLoader(data_dir=Path("/path/to/data"))
```

## Development

### Running Tests

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=imobench --cov-report=html
```

### Code Quality

```bash
# Format code
black src/ tests/

# Type checking
mypy src/

# Linting
ruff check src/ tests/
```

## Project Structure

```
imobench-pylib/
├── src/
│   └── imobench/
│       ├── __init__.py       # Public API
│       ├── types.py          # Data type definitions
│       ├── loader.py         # Loading functionality
│       ├── validators.py     # Data validation
│       └── exceptions.py     # Custom exceptions
├── tests/
│   ├── conftest.py          # Test configuration
│   ├── test_types.py        # Type tests
│   ├── test_validators.py   # Validation tests
│   ├── test_loader.py       # Loader tests
│   └── test_integration.py  # Integration tests
├── examples/                 # Usage examples
├── docs/                     # Documentation
├── setup.py                  # Package setup
├── pyproject.toml           # Project configuration
└── README.md                # This file
```

## License

This library is licensed under the Apache License 2.0. See the main repository for full license details.

## Citation

```bibtex
@inproceedings{luong-etal-2025-towards,
    title = "Towards Robust Mathematical Reasoning",
    author  = {Thang Luong and Dawsen Hwang and Hoang H. Nguyen and Golnaz Ghiasi and Yuri Chervonyi and Insuk Seo and Junsu Kim and Garrett Bingham and Jonathan Lee and Swaroop Mishra and Alex Zhai and Clara Huiyi Hu and Henryk Michalewski and Jimin Kim and Jeonghyun Ahn and Junhwi Bae and Xingyou Song and Trieu H. Trinh and Quoc V. Le and Junehyuk Jung},
    booktitle = "Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing",
    year = "2025",
    url = "https://aclanthology.org/2025.emnlp-main.1794/",
}
```

## Contributing

This library is maintained as part of the Google DeepMind Superhuman Reasoning project. For issues or contributions related to the datasets themselves, please see the main repository.

For library-specific issues or improvements, please open an issue describing:
- The problem or feature request
- Expected vs actual behavior
- Minimal reproducible example
- Python version and environment details

## Support

- **Documentation**: [https://imobench.github.io](https://imobench.github.io)
- **Issues**: [GitHub Issues](https://github.com/google-deepmind/superhuman/issues)
- **Repository**: [google-deepmind/superhuman](https://github.com/google-deepmind/superhuman)
