"""Health and metadata routes for version 1 API."""

from __future__ import annotations

from fastapi import APIRouter

from app.core.config import get_settings
from app.core.constants import (
    COURSE_CONCEPTS,
    KAGGLE_TRACK,
    PROJECT_DESCRIPTION,
    PROJECT_NAME,
    PROJECT_VERSION,
)

router = APIRouter(tags=["Health"])
settings = get_settings()


@router.get("/health")
def health_check() -> dict[str, str]:
    """Return the versioned service health state."""
    return {"status": "ok", "message": "CareerVerse Agent API v1 is running."}


@router.get("/metadata")
def metadata() -> dict[str, object]:
    """Return versioned project and runtime metadata."""
    return {
        "project": PROJECT_NAME,
        "description": PROJECT_DESCRIPTION,
        "version": PROJECT_VERSION,
        "track": KAGGLE_TRACK,
        "environment": settings.environment,
        "current_stage": "local_evaluation_pipeline",
        "course_concepts_demonstrated": COURSE_CONCEPTS,
    }
