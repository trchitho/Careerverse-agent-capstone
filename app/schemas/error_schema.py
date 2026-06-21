"""Structured error response schemas for CareerVerse Agent."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """Consistent schema for all application errors."""

    error: str
    message: str
    status_code: int
    details: dict[str, Any] | None = None
