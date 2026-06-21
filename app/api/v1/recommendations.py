"""Career recommendation routes for version 1 API."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from app.agents import CareerAdvisorAgent
from app.core.exceptions import UnsafeProfileError
from app.schemas import AgentRecommendationResponse, UserProfileRequest
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
