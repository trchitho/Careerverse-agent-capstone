"""FastAPI entrypoint for the CareerVerse Agent service."""

from fastapi import FastAPI, HTTPException, Query

from app.agents import CareerAdvisorAgent
from app.core.config import get_settings
from app.core.constants import (
    COURSE_CONCEPTS,
    KAGGLE_TRACK,
    PROJECT_DESCRIPTION,
    PROJECT_NAME,
    PROJECT_VERSION,
)
from app.schemas import (
    AgentRecommendationResponse,
    ProfileValidationResponse,
    UserProfileRequest,
    UserProfileSummary,
)

settings = get_settings()
career_advisor = CareerAdvisorAgent()
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
        "current_stage": "multi_agent_recommendation",
        "course_concepts_demonstrated": COURSE_CONCEPTS,
    }


@app.post("/profiles/validate", response_model=ProfileValidationResponse)
def validate_profile(profile: UserProfileRequest) -> ProfileValidationResponse:
    """Return a normalized profile without running recommendation logic."""
    summary = UserProfileSummary.model_validate(profile.model_dump())
    return ProfileValidationResponse(normalized_profile=summary)


@app.post("/recommend", response_model=AgentRecommendationResponse)
def recommend(
    profile: UserProfileRequest,
    top_k: int = Query(default=3, ge=1, le=10),
) -> AgentRecommendationResponse:
    """Run the deterministic multi-agent career guidance workflow."""
    try:
        payload = career_advisor.run(profile, top_k=top_k)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    return AgentRecommendationResponse.model_validate(payload)
