from __future__ import annotations

class AppError(Exception):
    """Base application error."""


class ValidationError(AppError):
    """Invalid input or configuration."""


class TransientError(AppError):
    """Retryable error for external/transient failures."""


class PermanentError(AppError):
    """Non-retryable business logic failure."""


class ExternalServiceError(TransientError):
    """External dependency failure (HTTP, S3, etc.)."""
