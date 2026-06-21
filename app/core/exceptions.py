"""Custom exceptions for CareerVerse Agent."""

from __future__ import annotations


class AppError(Exception):
    """Base application exception."""

    def __init__(self, message: str, status_code: int = 500) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class UnsafeProfileError(AppError):
    """Raised when profile safety validation fails."""

    def __init__(self, message: str, risk_level: str = "high") -> None:
        super().__init__(message, status_code=400)
        self.risk_level = risk_level


class ResourceNotFoundError(AppError):
    """Raised when a career or skill is not found."""

    def __init__(self, message: str) -> None:
        super().__init__(message, status_code=404)
