"""Schemas for career recommendation feedback and metrics."""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator


class RecommendationFeedbackRequest(BaseModel):
    """Payload to submit recommendation feedback."""

    session_id: str | None = Field(default=None, max_length=100)
    career_id: str | None = Field(default=None, max_length=100)
    career_title: str | None = Field(default=None, max_length=100)
    rating: int = Field(ge=1, le=5)
    helpful: bool
    comment: str | None = Field(default=None, max_length=300)
    source: str = Field(default="web", max_length=50)

    @field_validator("comment")
    @classmethod
    def sanitize_comment(cls, value: str | None) -> str | None:
        """Strip whitespace and perform basic input cleanup."""
        if value is None:
            return None
        cleaned = value.strip()
        lowered = cleaned.lower()
        if "ignore previous" in lowered or "system prompt" in lowered:
            cleaned = "[Redacted due to input safety warning]"
        return cleaned


class RecommendationFeedbackResponse(BaseModel):
    """Standard success response payload for feedback submission."""

    id: str
    created_at: str
    status: str = "submitted"


class FeedbackSummary(BaseModel):
    """Aggregate statistics for feedback submissions."""

    total_count: int
    average_rating: float
    helpful_count: int
    not_helpful_count: int


class MetricsSummaryResponse(BaseModel):
    """Global system status quality indicators and environment summary."""

    total_feedback_count: int
    average_rating: float
    helpful_count: int
    not_helpful_count: int
    data_source: str
    external_llm_enabled: bool
    app_version: str
    environment: str
