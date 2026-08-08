"""Tests for data validation functionality."""

import pytest
from imobench.validators import (
    validate_answerbench_row,
    validate_proofbench_row,
    validate_gradingbench_row,
    validate_dataset_counts,
)
from imobench.exceptions import ValidationError


# AnswerBench validation tests

def test_validate_answerbench_valid_row():
    """Test validation of a valid answerbench row."""
    row = {
        'Problem ID': 'imo-bench-algebra-001',
        'Problem': 'Find all $N$ such that...',
        'Short Answer': '3',
        'Category': 'Algebra',
        'Subcategory': 'Operation',
        'Source': 'IMO Shortlist 2021'
    }
    
    # Should not raise
    validate_answerbench_row(row)


def test_validate_answerbench_missing_field():
    """Test validation fails with missing field."""
    row = {
        'Problem ID': 'imo-bench-algebra-001',
        'Problem': 'Find all $N$ such that...',
        # Missing 'Short Answer'
        'Category': 'Algebra',
        'Subcategory': 'Operation',
        'Source': 'IMO Shortlist 2021'
    }
    
    with pytest.raises(ValidationError, match="Missing required fields"):
        validate_answerbench_row(row)


def test_validate_answerbench_empty_field():
    """Test validation fails with empty field."""
    row = {
        'Problem ID': 'imo-bench-algebra-001',
        'Problem': '',  # Empty
        'Short Answer': '3',
        'Category': 'Algebra',
        'Subcategory': 'Operation',
        'Source': 'IMO Shortlist 2021'
    }
    
    with pytest.raises(ValidationError, match="Empty value"):
        validate_answerbench_row(row)


def test_validate_answerbench_invalid_category():
    """Test validation fails with invalid category."""
    row = {
        'Problem ID': 'imo-bench-algebra-001',
        'Problem': 'Find all $N$ such that...',
        'Short Answer': '3',
        'Category': 'InvalidCategory',
        'Subcategory': 'Operation',
        'Source': 'IMO Shortlist 2021'
    }
    
    with pytest.raises(ValidationError, match="Invalid category"):
        validate_answerbench_row(row)


def test_validate_answerbench_invalid_id_format():
    """Test validation fails with invalid Problem ID format."""
    row = {
        'Problem ID': 'invalid-id-001',
        'Problem': 'Find all $N$ such that...',
        'Short Answer': '3',
        'Category': 'Algebra',
        'Subcategory': 'Operation',
        'Source': 'IMO Shortlist 2021'
    }
    
    with pytest.raises(ValidationError, match="Invalid Problem ID format"):
        validate_answerbench_row(row)


# ProofBench validation tests

def test_validate_proofbench_valid_row():
    """Test validation of a valid proofbench row."""
    row = {
        'Problem ID': 'PB-Basic-001',
        'Problem': 'Determine all functions...',
        'Solution': 'By taking $x = 0$...',
        'Grading guidelines': '(Partial) 1. Guessed...',
        'Category': 'Algebra',
        'Level': 'IMO-easy',
        'Short Answer': '$f(x) = 0$',
        'Source': 'IMO 2019, P1'
    }
    
    # Should not raise
    validate_proofbench_row(row)


def test_validate_proofbench_invalid_id():
    """Test validation fails with invalid Problem ID."""
    row = {
        'Problem ID': 'invalid-001',
        'Problem': 'Determine all functions...',
        'Solution': 'By taking $x = 0$...',
        'Grading guidelines': '(Partial) 1. Guessed...',
        'Category': 'Algebra',
        'Level': 'IMO-easy',
        'Short Answer': '$f(x) = 0$',
        'Source': 'IMO 2019, P1'
    }
    
    with pytest.raises(ValidationError, match="Invalid Problem ID format"):
        validate_proofbench_row(row)


# GradingBench validation tests

def test_validate_gradingbench_valid_row():
    """Test validation of a valid gradingbench row."""
    row = {
        'Grading ID': 'GB-0001',
        'Problem ID': 'PB-Advanced-001',
        'Problem': 'For a positive integer $n$...',
        'Solution': "Let's look at the following lemma...",
        'Grading guidelines': '(Partial) 1. Proved...',
        'Response': 'We will prove by induction...',
        'Points': '7',
        'Reward': 'Partial',
        'Problem Source': 'IMO Shortlist 2021'
    }
    
    # Should not raise
    validate_gradingbench_row(row)


def test_validate_gradingbench_invalid_points():
    """Test validation fails with invalid points."""
    row = {
        'Grading ID': 'GB-0001',
        'Problem ID': 'PB-Advanced-001',
        'Problem': 'For a positive integer $n$...',
        'Solution': "Let's look at the following lemma...",
        'Grading guidelines': '(Partial) 1. Proved...',
        'Response': 'We will prove by induction...',
        'Points': '15',  # Out of range
        'Reward': '0.85',
        'Problem Source': 'IMO Shortlist 2021'
    }
    
    with pytest.raises(ValidationError, match="Points must be between 0 and 10"):
        validate_gradingbench_row(row)


def test_validate_gradingbench_non_numeric_points():
    """Test validation fails with non-numeric points."""
    row = {
        'Grading ID': 'GB-0001',
        'Problem ID': 'PB-Advanced-001',
        'Problem': 'For a positive integer $n$...',
        'Solution': "Let's look at the following lemma...",
        'Grading guidelines': '(Partial) 1. Proved...',
        'Response': 'We will prove by induction...',
        'Points': 'seven',  # Not a number
        'Reward': 'Partial',
        'Problem Source': 'IMO Shortlist 2021'
    }
    
    with pytest.raises(ValidationError, match="Points must be an integer"):
        validate_gradingbench_row(row)


def test_validate_gradingbench_invalid_reward():
    """Test validation handles various reward values."""
    # Reward is now a categorical field, so any non-empty string is valid
    row = {
        'Grading ID': 'GB-0001',
        'Problem ID': 'PB-Advanced-001',
        'Problem': 'For a positive integer $n$...',
        'Solution': "Let's look at the following lemma...",
        'Grading guidelines': '(Partial) 1. Proved...',
        'Response': 'We will prove by induction...',
        'Points': '7',
        'Reward': 'Incorrect',  # Valid categorical value
        'Problem Source': 'IMO Shortlist 2021'
    }
    
    # Should not raise - categorical rewards are allowed
    validate_gradingbench_row(row)


# Dataset count validation tests

def test_validate_dataset_counts_valid():
    """Test validation of valid dataset counts."""
    # Should not raise
    validate_dataset_counts(
        answerbench_count=400,
        proofbench_count=60,
        gradingbench_count=1000
    )


def test_validate_dataset_counts_invalid_answerbench():
    """Test validation fails with invalid answerbench count."""
    with pytest.raises(ValidationError, match="Unexpected answerbench count"):
        validate_dataset_counts(
            answerbench_count=100,  # Too few
            proofbench_count=60,
            gradingbench_count=1000
        )


def test_validate_dataset_counts_invalid_proofbench():
    """Test validation fails with invalid proofbench count."""
    with pytest.raises(ValidationError, match="Unexpected proofbench count"):
        validate_dataset_counts(
            answerbench_count=400,
            proofbench_count=20,  # Too few
            gradingbench_count=1000
        )
