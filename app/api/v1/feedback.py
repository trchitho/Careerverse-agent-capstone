"""Feedback API routes for version 1 API."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.schemas.feedback_schema import (
    FeedbackSummary,
    RecommendationFeedbackRequest,
    RecommendationFeedbackResponse,
)
from app.services.feedback_service import (
    get_feedback_summary,
    submit_recommendation_feedback,
)

router = APIRouter(tags=["Feedback"])


@router.post("/feedback/recommendation", response_model=RecommendationFeedbackResponse, status_code=201)
def post_feedback(
    request: RecommendationFeedbackRequest,
) -> RecommendationFeedbackResponse:
    """Submit rating and comments regarding generated recommendation fits."""
    try:
        return submit_recommendation_feedback(request)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.get("/feedback/summary", response_model=FeedbackSummary)
def get_summary() -> FeedbackSummary:
    """Retrieve aggregate summary stats of all recommendation feedback."""
    return get_feedback_summary()
