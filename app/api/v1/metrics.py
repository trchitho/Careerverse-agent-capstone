"""Metrics and system quality API routes for version 1 API."""

from __future__ import annotations

from fastapi import APIRouter

from app.core.config import get_settings
from app.schemas.feedback_schema import MetricsSummaryResponse
from app.services.feedback_service import get_feedback_summary

router = APIRouter(tags=["Metrics"])
settings = get_settings()


@router.get("/metrics/summary", response_model=MetricsSummaryResponse)
def get_metrics_summary() -> MetricsSummaryResponse:
    """Retrieve system diagnostics, average recommendation scores, and configurations."""
    feedback = get_feedback_summary()
    return MetricsSummaryResponse(
        total_feedback_count=feedback.total_count,
        average_rating=feedback.average_rating,
        helpful_count=feedback.helpful_count,
        not_helpful_count=feedback.not_helpful_count,
        data_source=settings.data_source,
        external_llm_enabled=settings.enable_llm_explanations,
        app_version=settings.app_version,
        environment=settings.environment,
    )
