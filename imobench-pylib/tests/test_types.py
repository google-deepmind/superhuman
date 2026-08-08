"""Tests for IMO Bench data types."""

import pytest
from imobench.types import (
    AnswerBenchProblem,
    ProofBenchProblem,
    GradingBenchEntry,
)


def test_answerbench_problem_creation():
    """Test creating an AnswerBenchProblem."""
    problem = AnswerBenchProblem(
        problem_id="imo-bench-algebra-001",
        problem="Find all $N$ such that...",
        short_answer="3",
        category="Algebra",
        subcategory="Operation",
        source="IMO Shortlist 2021"
    )
    
    assert problem.problem_id == "imo-bench-algebra-001"
    assert problem.category == "Algebra"
    assert problem.subcategory == "Operation"


def test_answerbench_problem_immutable():
    """Test that AnswerBenchProblem is immutable."""
    problem = AnswerBenchProblem(
        problem_id="imo-bench-algebra-001",
        problem="Find all $N$ such that...",
        short_answer="3",
        category="Algebra",
        subcategory="Operation",
        source="IMO Shortlist 2021"
    )
    
    with pytest.raises(AttributeError):
        problem.category = "Geometry"


def test_answerbench_problem_repr():
    """Test AnswerBenchProblem string representation."""
    problem = AnswerBenchProblem(
        problem_id="imo-bench-algebra-001",
        problem="Find all $N$ such that...",
        short_answer="3",
        category="Algebra",
        subcategory="Operation",
        source="IMO Shortlist 2021"
    )
    
    repr_str = repr(problem)
    assert "imo-bench-algebra-001" in repr_str
    assert "Algebra" in repr_str


def test_proofbench_problem_creation():
    """Test creating a ProofBenchProblem."""
    problem = ProofBenchProblem(
        problem_id="PB-Basic-001",
        problem="Determine all functions...",
        solution="By taking $x = 0$...",
        grading_guidelines="(Partial) 1. Guessed...",
        category="Algebra",
        level="IMO-easy",
        short_answer="$f(x) = 0$ and $f(x) = 2x + c$",
        source="IMO 2019, P1"
    )
    
    assert problem.problem_id == "PB-Basic-001"
    assert problem.level == "IMO-easy"
    assert problem.category == "Algebra"


def test_gradingbench_entry_creation():
    """Test creating a GradingBenchEntry."""
    entry = GradingBenchEntry(
        grading_id="GB-0001",
        problem_id="PB-Advanced-001",
        problem="For a positive integer $n$...",
        solution="Let's look at the following lemma...",
        grading_guidelines="(Partial) 1. Proved...",
        response="We will prove by induction...",
        points=7,
        reward="Partial",
        problem_source="IMO Shortlist 2021"
    )
    
    assert entry.grading_id == "GB-0001"
    assert entry.points == 7
    assert entry.reward == "Partial"


def test_gradingbench_entry_repr():
    """Test GradingBenchEntry string representation."""
    entry = GradingBenchEntry(
        grading_id="GB-0001",
        problem_id="PB-Advanced-001",
        problem="For a positive integer $n$...",
        solution="Let's look at the following lemma...",
        grading_guidelines="(Partial) 1. Proved...",
        response="We will prove by induction...",
        points=7,
        reward="Partial",
        problem_source="IMO Shortlist 2021"
    )
    
    repr_str = repr(entry)
    assert "GB-0001" in repr_str
    assert "7" in repr_str
