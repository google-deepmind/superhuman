"""Data loading functionality for IMO Bench datasets."""

import csv
from pathlib import Path
from typing import Iterator, Optional, Callable

from .types import (
    AnswerBenchProblem,
    ProofBenchProblem,
    GradingBenchEntry,
    AnswerBenchDataset,
    ProofBenchDataset,
    GradingBenchDataset,
)
from .exceptions import DataLoadError, FileNotFoundError as IMOFileNotFoundError
from .validators import (
    validate_answerbench_row,
    validate_proofbench_row,
    validate_gradingbench_row,
)


class IMOBenchLoader:
    """Main loader class for IMO Bench datasets.
    
    This class provides methods to load datasets from CSV files with
    support for filtering, lazy loading, and validation.
    
    Args:
        data_dir: Path to the directory containing CSV files.
                  Defaults to looking for '../imobench' relative to package.
    
    Example:
        >>> loader = IMOBenchLoader()
        >>> problems = loader.load_answerbench(category="Algebra")
        >>> print(f"Loaded {len(problems)} algebra problems")
    """
    
    def __init__(self, data_dir: Optional[Path] = None):
        if data_dir is None:
            # Default: look for imobench directory at repo root
            package_dir = Path(__file__).parent
            data_dir = package_dir.parent.parent.parent / "imobench"
        
        self.data_dir = Path(data_dir)
        if not self.data_dir.exists():
            raise IMOFileNotFoundError(
                f"Data directory not found: {self.data_dir}\n"
                f"Please provide the correct path to the imobench directory."
            )
    
    def _load_csv(self, filename: str) -> list[dict[str, str]]:
        """Load a CSV file and return rows as dictionaries."""
        filepath = self.data_dir / filename
        
        if not filepath.exists():
            raise IMOFileNotFoundError(
                f"Dataset file not found: {filepath}\n"
                f"Expected location: {filepath}"
            )
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                return list(reader)
        except Exception as e:
            raise DataLoadError(f"Error reading {filename}: {e}") from e
    
    def load_answerbench(
        self,
        category: Optional[str] = None,
        subcategory: Optional[str] = None,
        source: Optional[str] = None,
        validate: bool = True,
    ) -> AnswerBenchDataset:
        """Load IMO-AnswerBench dataset.
        
        Args:
            category: Filter by category (e.g., "Algebra", "Geometry")
            subcategory: Filter by subcategory
            source: Filter by source (e.g., "IMO Shortlist 2021")
            validate: Whether to validate each row
        
        Returns:
            List of AnswerBenchProblem objects
        
        Raises:
            DataLoadError: If the file cannot be loaded
            ValidationError: If validation is enabled and data is invalid
        """
        rows = self._load_csv("answerbench.csv")
        problems = []
        
        for row in rows:
            if validate:
                validate_answerbench_row(row)
            
            # Apply filters
            if category and row['Category'] != category:
                continue
            if subcategory and row['Subcategory'] != subcategory:
                continue
            if source and row['Source'] != source:
                continue
            
            problem = AnswerBenchProblem(
                problem_id=row['Problem ID'],
                problem=row['Problem'],
                short_answer=row['Short Answer'],
                category=row['Category'],
                subcategory=row['Subcategory'],
                source=row['Source'],
            )
            problems.append(problem)
        
        return problems
    
    def load_proofbench(
        self,
        category: Optional[str] = None,
        level: Optional[str] = None,
        validate: bool = True,
    ) -> ProofBenchDataset:
        """Load IMO-ProofBench dataset.
        
        Args:
            category: Filter by category (e.g., "Algebra", "Geometry")
            level: Filter by difficulty level (e.g., "IMO-easy", "pre-IMO")
            validate: Whether to validate each row
        
        Returns:
            List of ProofBenchProblem objects
        
        Raises:
            DataLoadError: If the file cannot be loaded
            ValidationError: If validation is enabled and data is invalid
        """
        rows = self._load_csv("proofbench.csv")
        problems = []
        
        for row in rows:
            if validate:
                validate_proofbench_row(row)
            
            # Apply filters
            if category and row['Category'] != category:
                continue
            if level and row['Level'] != level:
                continue
            
            problem = ProofBenchProblem(
                problem_id=row['Problem ID'],
                problem=row['Problem'],
                solution=row['Solution'],
                grading_guidelines=row['Grading guidelines'],
                category=row['Category'],
                level=row['Level'],
                short_answer=row['Short Answer'],
                source=row['Source'],
            )
            problems.append(problem)
        
        return problems
    
    def load_gradingbench(
        self,
        problem_id: Optional[str] = None,
        min_points: Optional[int] = None,
        max_points: Optional[int] = None,
        validate: bool = True,
        lazy: bool = False,
    ) -> GradingBenchDataset | Iterator[GradingBenchEntry]:
        """Load IMO-GradingBench dataset.
        
        Note: This dataset is large (186K lines). Consider using lazy=True
        for memory-efficient iteration.
        
        Args:
            problem_id: Filter by problem ID
            min_points: Filter by minimum points awarded
            max_points: Filter by maximum points awarded
            validate: Whether to validate each row
            lazy: If True, return an iterator instead of loading all data
        
        Returns:
            List of GradingBenchEntry objects, or Iterator if lazy=True
        
        Raises:
            DataLoadError: If the file cannot be loaded
            ValidationError: If validation is enabled and data is invalid
        """
        if lazy:
            return self._iter_gradingbench(
                problem_id=problem_id,
                min_points=min_points,
                max_points=max_points,
                validate=validate,
            )
        
        rows = self._load_csv("gradingbench.csv")
        entries = []
        
        for row in rows:
            if validate:
                validate_gradingbench_row(row)
            
            # Parse numeric fields
            try:
                points = int(row['Points'])
                reward = row['Reward'].strip()
            except (ValueError, KeyError) as e:
                if validate:
                    raise DataLoadError(f"Invalid field: {e}") from e
                continue
            
            # Apply filters
            if problem_id and row['Problem ID'] != problem_id:
                continue
            if min_points is not None and points < min_points:
                continue
            if max_points is not None and points > max_points:
                continue
            
            entry = GradingBenchEntry(
                grading_id=row['Grading ID'],
                problem_id=row['Problem ID'],
                problem=row['Problem'],
                solution=row['Solution'],
                grading_guidelines=row['Grading guidelines'],
                response=row['Response'],
                points=points,
                reward=reward,
                problem_source=row['Problem Source'],
            )
            entries.append(entry)
        
        return entries
    
    def _iter_gradingbench(
        self,
        problem_id: Optional[str] = None,
        min_points: Optional[int] = None,
        max_points: Optional[int] = None,
        validate: bool = True,
    ) -> Iterator[GradingBenchEntry]:
        """Lazy iterator for gradingbench dataset."""
        filepath = self.data_dir / "gradingbench.csv"
        
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                if validate:
                    validate_gradingbench_row(row)
                
                try:
                    points = int(row['Points'])
                    reward = row['Reward'].strip()
                except (ValueError, KeyError):
                    if validate:
                        raise
                    continue
                
                # Apply filters
                if problem_id and row['Problem ID'] != problem_id:
                    continue
                if min_points is not None and points < min_points:
                    continue
                if max_points is not None and points > max_points:
                    continue
                
                yield GradingBenchEntry(
                    grading_id=row['Grading ID'],
                    problem_id=row['Problem ID'],
                    problem=row['Problem'],
                    solution=row['Solution'],
                    grading_guidelines=row['Grading guidelines'],
                    response=row['Response'],
                    points=points,
                    reward=reward,
                    problem_source=row['Problem Source'],
                )


# Convenience functions using default loader
_default_loader: Optional[IMOBenchLoader] = None


def _get_default_loader() -> IMOBenchLoader:
    """Get or create the default loader instance."""
    global _default_loader
    if _default_loader is None:
        _default_loader = IMOBenchLoader()
    return _default_loader


def load_answerbench(**kwargs) -> AnswerBenchDataset:
    """Load IMO-AnswerBench using default loader.
    
    See IMOBenchLoader.load_answerbench() for arguments.
    """
    return _get_default_loader().load_answerbench(**kwargs)


def load_proofbench(**kwargs) -> ProofBenchDataset:
    """Load IMO-ProofBench using default loader.
    
    See IMOBenchLoader.load_proofbench() for arguments.
    """
    return _get_default_loader().load_proofbench(**kwargs)


def load_gradingbench(**kwargs) -> GradingBenchDataset | Iterator[GradingBenchEntry]:
    """Load IMO-GradingBench using default loader.
    
    See IMOBenchLoader.load_gradingbench() for arguments.
    """
    return _get_default_loader().load_gradingbench(**kwargs)
