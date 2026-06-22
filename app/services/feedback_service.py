"""Service for processing recommendation feedback and analytics."""

from __future__ import annotations

from app.repositories import InMemoryFeedbackRepository
from app.schemas.feedback_schema import (
    FeedbackSummary,
    RecommendationFeedbackRequest,
    RecommendationFeedbackResponse,
)

_feedback_repo = InMemoryFeedbackRepository()


def submit_recommendation_feedback(
    request: RecommendationFeedbackRequest,
) -> RecommendationFeedbackResponse:
    """Validate safety constraints and write recommendation feedback snapshot."""
    comment = request.comment
    if comment:
        comment_clean = comment.strip()
        if len(comment_clean) > 300:
            raise ValueError("Comment must not exceed 300 characters.")
        lowered = comment_clean.lower()
        if "ignore previous" in lowered or "system prompt" in lowered:
            comment_clean = "[Redacted due to input safety warning]"
        comment = comment_clean

    record = _feedback_repo.save(
        session_id=request.session_id,
        career_id=request.career_id,
        career_title=request.career_title,
        rating=request.rating,
        helpful=request.helpful,
        comment=comment,
        source=request.source,
    )
    return RecommendationFeedbackResponse(
        id=record["id"],
        created_at=record["created_at"],
    )


def get_feedback_summary() -> FeedbackSummary:
    """Retrieve aggregate summary stats of all recommendation feedbacks."""
    data = _feedback_repo.summary()
    return FeedbackSummary(
        total_count=data["total_count"],
        average_rating=data["average_rating"],
        helpful_count=data["helpful_count"],
        not_helpful_count=data["not_helpful_count"],
    )
