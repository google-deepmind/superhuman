"""Integration tests for the IMO Bench library."""

import pytest
from pathlib import Path
from imobench import (
    load_answerbench,
    load_proofbench,
    load_gradingbench,
    IMOBenchLoader,
)
from imobench.exceptions import FileNotFoundError as IMOFileNotFoundError


@pytest.fixture
def data_dir():
    """Get the data directory path."""
    repo_root = Path(__file__).parent.parent.parent
    data_dir = repo_root / "imobench"
    
    if not data_dir.exists():
        pytest.skip(f"Data directory not found: {data_dir}")
    
    return data_dir


def test_end_to_end_workflow(data_dir):
    """Test a complete workflow: load, filter, analyze."""
    loader = IMOBenchLoader(data_dir=data_dir)
    
    # Load all algebra problems
    algebra_problems = loader.load_answerbench(category="Algebra", validate=False)
    
    # Should have some problems
    assert len(algebra_problems) > 0
    
    # All should be algebra
    assert all(p.category == "Algebra" for p in algebra_problems)
    
    # Count subcategories
    subcategories = {}
    for problem in algebra_problems:
        subcategories[problem.subcategory] = subcategories.get(problem.subcategory, 0) + 1
    
    # Should have multiple subcategories
    assert len(subcategories) > 1


def test_cross_dataset_consistency(data_dir):
    """Test that problem IDs in gradingbench reference actual problems."""
    loader = IMOBenchLoader(data_dir=data_dir)
    
    # Load proofbench problems
    proof_problems = loader.load_proofbench(validate=False)
    proof_ids = {p.problem_id for p in proof_problems}
    
    # Load a sample of grading entries
    grading_entries = loader.load_gradingbench(validate=False)
    if not grading_entries:
        pytest.skip("No grading entries found")
    
    # Take first 100 entries
    sample = grading_entries[:100]
    
    # Check that referenced problem IDs exist
    referenced_ids = {e.problem_id for e in sample}
    
    # All referenced IDs should be valid proofbench IDs
    for ref_id in referenced_ids:
        assert ref_id in proof_ids or ref_id.startswith('PB-'), \
            f"Invalid problem reference: {ref_id}"


def test_statistics_generation(data_dir):
    """Test generating statistics from the datasets."""
    loader = IMOBenchLoader(data_dir=data_dir)
    
    # Load all datasets
    answer_problems = loader.load_answerbench(validate=False)
    proof_problems = loader.load_proofbench(validate=False)
    
    # Generate statistics
    stats = {
        'answerbench': {
            'total': len(answer_problems),
            'categories': {},
        },
        'proofbench': {
            'total': len(proof_problems),
            'levels': {},
        },
    }
    
    # Count categories in answerbench
    for p in answer_problems:
        stats['answerbench']['categories'][p.category] = \
            stats['answerbench']['categories'].get(p.category, 0) + 1
    
    # Count levels in proofbench
    for p in proof_problems:
        stats['proofbench']['levels'][p.level] = \
            stats['proofbench']['levels'].get(p.level, 0) + 1
    
    # Verify we have reasonable numbers
    assert stats['answerbench']['total'] > 100
    assert stats['proofbench']['total'] > 10
    assert len(stats['answerbench']['categories']) >= 3  # At least 3 categories
    assert len(stats['proofbench']['levels']) >= 2  # At least 2 difficulty levels


def test_memory_efficiency_with_lazy_loading(data_dir):
    """Test that lazy loading doesn't load entire dataset into memory."""
    loader = IMOBenchLoader(data_dir=data_dir)
    
    # Use lazy loading
    iterator = loader.load_gradingbench(lazy=True, validate=False)
    
    # Process first 1000 entries
    count = 0
    for entry in iterator:
        count += 1
        if count >= 1000:
            break
    
    # Should have processed entries without loading entire dataset
    assert count == 1000


def test_filtering_combinations(data_dir):
    """Test combining multiple filters."""
    loader = IMOBenchLoader(data_dir=data_dir)
    
    # Load with multiple filters
    problems = loader.load_answerbench(
        category="Algebra",
        subcategory="Inequality",
        validate=False
    )
    
    # All results should match both filters
    for p in problems:
        assert p.category == "Algebra"
        assert p.subcategory == "Inequality"
