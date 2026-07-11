class StudentsPerformanceError(Exception):
    """Base exception for the project."""


class DataValidationError(StudentsPerformanceError):
    """Raised when source data or request payloads fail validation."""


class ModelArtifactError(StudentsPerformanceError):
    """Raised when a trained artifact is missing, stale, or invalid."""


class PredictionError(StudentsPerformanceError):
    """Raised when a prediction request cannot be scored."""


class TrainingError(StudentsPerformanceError):
    """Raised when the training workflow fails unexpectedly."""
