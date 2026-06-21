"""Career recommendation routes for version 1 API."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from app.agents import CareerAdvisorAgent
from app.core.exceptions import UnsafeProfileError
from app.models import SavedRecommendation
from app.schemas import AgentRecommendationResponse, UserProfileRequest
from app.services.saved_recommendation_service import (
    create_saved_recommendation,
    list_saved_recommendations,
)
from app.tools.safety_tools import get_safety_notice, validate_profile_safety

router = APIRouter(tags=["Recommendations"])
career_advisor = CareerAdvisorAgent()


@router.post("/recommend", response_model=AgentRecommendationResponse)
def recommend(
    profile: UserProfileRequest,
    top_k: int = Query(default=3, ge=1, le=10),
) -> AgentRecommendationResponse:
    """Run the deterministic multi-agent career guidance workflow."""
    safety_result = validate_profile_safety(profile)
    if not safety_result["is_safe"]:
        raise UnsafeProfileError(
            message=safety_result["safe_message"],
            risk_level=safety_result["risk_level"],
        )
    try:
        payload = career_advisor.run(safety_result["redacted_profile"], top_k=top_k)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    payload["safety_notice"] = get_safety_notice()
    return AgentRecommendationResponse.model_validate(payload)


class SaveRecommendationRequest(BaseModel):
    """Request payload to save a recommendation snapshot."""

    session_id: str
    recommendation_response: dict[str, Any]


@router.post("/recommendations/save", response_model=SavedRecommendation)
def save_recommendation(request: SaveRecommendationRequest) -> SavedRecommendation:
    """Save a recommendation response snapshot for a given session ID."""
    try:
        return create_saved_recommendation(
            session_id=request.session_id,
            recommendation_response=request.recommendation_response,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.get(
    "/recommendations/saved/{session_id}",
    response_model=list[SavedRecommendation],
)
def list_saved(session_id: str) -> list[SavedRecommendation]:
    """Retrieve saved recommendations for a given session ID."""
    try:
        return list_saved_recommendations(session_id)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
