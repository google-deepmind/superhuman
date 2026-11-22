"""Type definitions for IMO Bench datasets."""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class AnswerBenchProblem:
    """A problem from IMO-AnswerBench.
    
    Attributes:
        problem_id: Unique identifier (e.g., "imo-bench-algebra-001")
        problem: The problem statement in LaTeX format
        short_answer: The expected answer
        category: Main category (Algebra, Combinatorics, Geometry, Number theory)
        subcategory: Specific subcategory within the main category
        source: Original source of the problem
    """
    problem_id: str
    problem: str
    short_answer: str
    category: str
    subcategory: str
    source: str

    def __repr__(self) -> str:
        return f"AnswerBenchProblem(id='{self.problem_id}', category='{self.category}')"


@dataclass(frozen=True)
class ProofBenchProblem:
    """A problem from IMO-ProofBench.
    
    Attributes:
        problem_id: Unique identifier (e.g., "PB-Basic-001")
        problem: The problem statement in LaTeX format
        solution: Reference solution
        grading_guidelines: Guidelines for grading partial solutions
        category: Main category (Algebra, Combinatorics, Geometry, Number theory)
        level: Difficulty level (e.g., "IMO-easy", "pre-IMO", "IMO-hard")
        short_answer: Brief expected answer
        source: Original source of the problem
    """
    problem_id: str
    problem: str
    solution: str
    grading_guidelines: str
    category: str
    level: str
    short_answer: str
    source: str

    def __repr__(self) -> str:
        return f"ProofBenchProblem(id='{self.problem_id}', level='{self.level}')"


@dataclass(frozen=True)
class GradingBenchEntry:
    """An entry from IMO-GradingBench.
    
    Attributes:
        grading_id: Unique identifier (e.g., "GB-0001")
        problem_id: Reference to the problem being graded
        problem: The problem statement
        solution: Reference solution
        grading_guidelines: Grading criteria
        response: The response being graded
        points: Points awarded (0-10 scale)
        reward: Reward category (e.g., "Correct", "Partial", "Incorrect", "Almost")
        problem_source: Original source of the problem
    """
    grading_id: str
    problem_id: str
    problem: str
    solution: str
    grading_guidelines: str
    response: str
    points: int
    reward: str
    problem_source: str

    def __repr__(self) -> str:
        return f"GradingBenchEntry(id='{self.grading_id}', points={self.points})"


# Type aliases for collections
AnswerBenchDataset = list[AnswerBenchProblem]
ProofBenchDataset = list[ProofBenchProblem]
GradingBenchDataset = list[GradingBenchEntry]
