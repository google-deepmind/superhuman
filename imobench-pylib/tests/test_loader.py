"""Tests for data loading functionality."""

import pytest
from pathlib import Path
from imobench.loader import IMOBenchLoader
from imobench.types import (
    AnswerBenchProblem,
    ProofBenchProblem,
    GradingBenchEntry,
)
from imobench.exceptions import FileNotFoundError as IMOFileNotFoundError


@pytest.fixture
def loader():
    """Create a loader instance pointing to the actual data."""
    # Assumes tests are run from repo root or with proper PYTHONPATH
    repo_root = Path(__file__).parent.parent.parent
    data_dir = repo_root / "imobench"
    
    if not data_dir.exists():
        pytest.skip(f"Data directory not found: {data_dir}")
    
    return IMOBenchLoader(data_dir=data_dir)


def test_loader_invalid_data_dir():
    """Test that loader raises error with invalid data directory."""
    with pytest.raises(IMOFileNotFoundError):
        IMOBenchLoader(data_dir=Path("/nonexistent/path"))


def test_load_answerbench(loader):
    """Test loading answerbench dataset."""
    problems = loader.load_answerbench(validate=False)
    
    assert len(problems) > 0
    assert all(isinstance(p, AnswerBenchProblem) for p in problems)
    
    # Check first problem has expected structure
    first = problems[0]
    assert first.problem_id.startswith('imo-bench-')
    assert first.category in ['Algebra', 'Combinatorics', 'Geometry', 'Number theory']


def test_load_answerbench_with_category_filter(loader):
    """Test loading answerbench with category filter."""
    algebra_problems = loader.load_answerbench(category="Algebra", validate=False)
    
    assert len(algebra_problems) > 0
    assert all(p.category == "Algebra" for p in algebra_problems)


def test_load_answerbench_with_source_filter(loader):
    """Test loading answerbench with source filter."""
    problems = loader.load_answerbench(source="IMO Shortlist 2021", validate=False)
    
    # May or may not have results depending on data
    if problems:
        assert all(p.source == "IMO Shortlist 2021" for p in problems)


def test_load_proofbench(loader):
    """Test loading proofbench dataset."""
    problems = loader.load_proofbench(validate=False)
    
    assert len(problems) > 0
    assert all(isinstance(p, ProofBenchProblem) for p in problems)
    
    # Check first problem has expected structure
    first = problems[0]
    assert first.problem_id.startswith('PB-')
    assert first.category in ['Algebra', 'Combinatorics', 'Geometry', 'Number theory']
    assert first.level  # Should have a level


def test_load_proofbench_with_level_filter(loader):
    """Test loading proofbench with level filter."""
    problems = loader.load_proofbench(level="IMO-easy", validate=False)
    
    # May or may not have results depending on data
    if problems:
        assert all(p.level == "IMO-easy" for p in problems)


def test_load_gradingbench(loader):
    """Test loading gradingbench dataset."""
    # Load just a small subset for testing
    entries = loader.load_gradingbench(max_points=2, validate=False)
    
    assert len(entries) > 0
    assert all(isinstance(e, GradingBenchEntry) for e in entries)
    assert all(e.points <= 2 for e in entries)


def test_load_gradingbench_lazy(loader):
    """Test lazy loading of gradingbench dataset."""
    iterator = loader.load_gradingbench(min_points=5, lazy=True, validate=False)
    
    # Get first few entries
    entries = []
    for i, entry in enumerate(iterator):
        entries.append(entry)
        if i >= 10:  # Stop after 10
            break
    
    assert len(entries) > 0
    assert all(isinstance(e, GradingBenchEntry) for e in entries)
    assert all(e.points >= 5 for e in entries)


def test_load_gradingbench_with_problem_filter(loader):
    """Test loading gradingbench filtered by problem ID."""
    # First get a problem ID
    all_entries = loader.load_gradingbench(validate=False)
    if not all_entries:
        pytest.skip("No grading entries found")
    
    problem_id = all_entries[0].problem_id
    
    # Load entries for that problem
    filtered = loader.load_gradingbench(problem_id=problem_id, validate=False)
    
    assert len(filtered) > 0
    assert all(e.problem_id == problem_id for e in filtered)


def test_convenience_functions():
    """Test convenience functions work."""
    from imobench import load_answerbench, load_proofbench, load_gradingbench
    
    # These should work if data directory is in expected location
    try:
        problems = load_answerbench(validate=False)
        assert len(problems) > 0
    except IMOFileNotFoundError:
        pytest.skip("Data directory not in default location")
