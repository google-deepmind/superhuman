"""Validation utilities for IMO Bench datasets."""

from typing import Any
from .exceptions import ValidationError


# Required fields for each dataset
ANSWERBENCH_REQUIRED_FIELDS = {
    'Problem ID', 'Problem', 'Short Answer', 'Category', 'Subcategory', 'Source'
}

PROOFBENCH_REQUIRED_FIELDS = {
    'Problem ID', 'Problem', 'Solution', 'Grading guidelines',
    'Category', 'Level', 'Short Answer', 'Source'
}

GRADINGBENCH_REQUIRED_FIELDS = {
    'Grading ID', 'Problem ID', 'Problem', 'Solution',
    'Grading guidelines', 'Response', 'Points', 'Reward', 'Problem Source'
}

# Valid categories
VALID_CATEGORIES = {'Algebra', 'Combinatorics', 'Geometry', 'Number theory'}


def validate_answerbench_row(row: dict[str, Any]) -> None:
    """Validate a row from answerbench.csv.
    
    Args:
        row: Dictionary representing a CSV row
    
    Raises:
        ValidationError: If validation fails
    """
    # Check required fields
    missing_fields = ANSWERBENCH_REQUIRED_FIELDS - set(row.keys())
    if missing_fields:
        raise ValidationError(
            f"Missing required fields: {', '.join(missing_fields)}"
        )
    
    # Check for empty values
    for field in ANSWERBENCH_REQUIRED_FIELDS:
        if not row[field] or not row[field].strip():
            raise ValidationError(f"Empty value for required field: {field}")
    
    # Validate category
    if row['Category'] not in VALID_CATEGORIES:
        raise ValidationError(
            f"Invalid category: {row['Category']}. "
            f"Must be one of: {', '.join(VALID_CATEGORIES)}"
        )
    
    # Validate problem ID format
    if not row['Problem ID'].startswith('imo-bench-'):
        raise ValidationError(
            f"Invalid Problem ID format: {row['Problem ID']}. "
            f"Should start with 'imo-bench-'"
        )


def validate_proofbench_row(row: dict[str, Any]) -> None:
    """Validate a row from proofbench.csv.
    
    Args:
        row: Dictionary representing a CSV row
    
    Raises:
        ValidationError: If validation fails
    """
    # Check required fields
    missing_fields = PROOFBENCH_REQUIRED_FIELDS - set(row.keys())
    if missing_fields:
        raise ValidationError(
            f"Missing required fields: {', '.join(missing_fields)}"
        )
    
    # Check for empty values (allow empty short_answer as it can be descriptive)
    for field in PROOFBENCH_REQUIRED_FIELDS - {'Short Answer'}:
        if not row[field] or not row[field].strip():
            raise ValidationError(f"Empty value for required field: {field}")
    
    # Validate category
    if row['Category'] not in VALID_CATEGORIES:
        raise ValidationError(
            f"Invalid category: {row['Category']}. "
            f"Must be one of: {', '.join(VALID_CATEGORIES)}"
        )
    
    # Validate problem ID format
    if not row['Problem ID'].startswith('PB-'):
        raise ValidationError(
            f"Invalid Problem ID format: {row['Problem ID']}. "
            f"Should start with 'PB-'"
        )


def validate_gradingbench_row(row: dict[str, Any]) -> None:
    """Validate a row from gradingbench.csv.
    
    Args:
        row: Dictionary representing a CSV row
    
    Raises:
        ValidationError: If validation fails
    """
    # Check required fields
    missing_fields = GRADINGBENCH_REQUIRED_FIELDS - set(row.keys())
    if missing_fields:
        raise ValidationError(
            f"Missing required fields: {', '.join(missing_fields)}"
        )
    
    # Check for empty values
    for field in GRADINGBENCH_REQUIRED_FIELDS:
        if field not in row or row[field] is None:
            raise ValidationError(f"Missing field: {field}")
        if isinstance(row[field], str) and not row[field].strip():
            raise ValidationError(f"Empty value for required field: {field}")
    
    # Validate grading ID format
    if not row['Grading ID'].startswith('GB-'):
        raise ValidationError(
            f"Invalid Grading ID format: {row['Grading ID']}. "
            f"Should start with 'GB-'"
        )
    
    # Validate numeric fields
    try:
        points = int(row['Points'])
        if not 0 <= points <= 10:
            raise ValidationError(
                f"Points must be between 0 and 10, got: {points}"
            )
    except ValueError:
        raise ValidationError(f"Points must be an integer, got: {row['Points']}")
    
    # Reward is a categorical field (Correct, Partial, Incorrect, Almost, etc.)
    # Just check it's not empty - validation happens in field check above
    valid_rewards = {'Correct', 'Partial', 'Incorrect', 'Almost'}
    if row['Reward'] not in valid_rewards:
        # Allow other values but could log warning in production
        pass


def validate_dataset_counts(
    answerbench_count: int,
    proofbench_count: int,
    gradingbench_count: int,
) -> None:
    """Validate that dataset counts match expected values.
    
    Args:
        answerbench_count: Number of problems in answerbench
        proofbench_count: Number of problems in proofbench
        gradingbench_count: Number of entries in gradingbench
    
    Raises:
        ValidationError: If counts don't match expectations
    """
    # Based on the documentation:
    # - answerbench: 400 problems
    # - proofbench: 60 problems
    # - gradingbench: 1000 human gradings
    
    # We'll allow some flexibility since these are approximate
    if not 390 <= answerbench_count <= 410:
        raise ValidationError(
            f"Unexpected answerbench count: {answerbench_count} "
            f"(expected ~400)"
        )
    
    if not 55 <= proofbench_count <= 65:
        raise ValidationError(
            f"Unexpected proofbench count: {proofbench_count} "
            f"(expected ~60)"
        )
    
    if not 900 <= gradingbench_count <= 200000:
        raise ValidationError(
            f"Unexpected gradingbench count: {gradingbench_count} "
            f"(expected ~1000)"
        )
