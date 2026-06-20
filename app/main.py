"""FastAPI entrypoint for the CareerVerse Agent service."""

from fastapi import FastAPI

from app.core.config import get_settings
from app.core.constants import (
    COURSE_CONCEPTS,
    KAGGLE_TRACK,
    PROJECT_DESCRIPTION,
    PROJECT_NAME,
    PROJECT_VERSION,
)
from app.schemas import (
    ProfileValidationResponse,
    UserProfileRequest,
    UserProfileSummary,
)

settings = get_settings()
app = FastAPI(
    title=settings.app_name,
    description=PROJECT_DESCRIPTION,
    version=settings.app_version,
)


@app.get("/")
def health_check() -> dict[str, str]:
    """Return the public service health state."""
    return {"status": "ok", "message": "CareerVerse Agent is running."}


@app.get("/metadata")
def metadata() -> dict[str, object]:
    """Return public project and runtime metadata."""
    return {
        "project": PROJECT_NAME,
        "description": PROJECT_DESCRIPTION,
        "version": PROJECT_VERSION,
        "track": KAGGLE_TRACK,
        "environment": settings.environment,
        "current_stage": "schemas_and_input_validation",
        "course_concepts_demonstrated": COURSE_CONCEPTS,
    }


@app.post("/profiles/validate", response_model=ProfileValidationResponse)
def validate_profile(profile: UserProfileRequest) -> ProfileValidationResponse:
    """Return a normalized profile without running recommendation logic."""
    summary = UserProfileSummary.model_validate(profile.model_dump())
    return ProfileValidationResponse(normalized_profile=summary)
