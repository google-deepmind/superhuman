"""IMO Bench - Python library for loading and working with IMO Bench datasets.

This package provides utilities for loading, validating, and working with
the IMO Bench mathematical reasoning benchmarks, including:
- IMO-AnswerBench: 400 challenging short-answer problems
- IMO-ProofBench: 60 proof-based problems
- IMO-GradingBench: 1000 human gradings for evaluation

Example:
    >>> from imobench import load_answerbench, load_proofbench
    >>> problems = load_answerbench()
    >>> for problem in problems[:5]:
    ...     print(f"{problem.problem_id}: {problem.category}")
"""

__version__ = "0.1.0"
__author__ = "IMO Bench Contributors"
__all__ = [
    "load_answerbench",
    "load_proofbench", 
    "load_gradingbench",
    "AnswerBenchProblem",
    "ProofBenchProblem",
    "GradingBenchEntry",
    "IMOBenchLoader",
    "ValidationError",
]

from .loader import (
    load_answerbench,
    load_proofbench,
    load_gradingbench,
    IMOBenchLoader,
)
from .types import (
    AnswerBenchProblem,
    ProofBenchProblem,
    GradingBenchEntry,
)
from .exceptions import ValidationError
