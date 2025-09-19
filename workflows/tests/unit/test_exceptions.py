from __future__ import annotations

from app.exceptions import AppError, ValidationError, TransientError, PermanentError, ExternalServiceError


def test_exception_hierarchy():
    assert issubclass(ValidationError, AppError)
    assert issubclass(TransientError, AppError)
    assert issubclass(PermanentError, AppError)
    assert issubclass(ExternalServiceError, TransientError)
