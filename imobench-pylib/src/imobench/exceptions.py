"""Custom exceptions for IMO Bench library."""


class IMOBenchError(Exception):
    """Base exception for all IMO Bench errors."""
    pass


class ValidationError(IMOBenchError):
    """Raised when data validation fails."""
    pass


class DataLoadError(IMOBenchError):
    """Raised when data cannot be loaded."""
    pass


class FileNotFoundError(DataLoadError):
    """Raised when a dataset file cannot be found."""
    pass
