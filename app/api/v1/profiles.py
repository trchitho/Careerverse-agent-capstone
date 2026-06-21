"""Profile validation routes for version 1 API."""

from __future__ import annotations

from fastapi import APIRouter

from app.schemas import ProfileValidationResponse, UserProfileRequest, UserProfileSummary

router = APIRouter(tags=["Profiles"])


@router.post("/profiles/validate", response_model=ProfileValidationResponse)
def validate_profile(profile: UserProfileRequest) -> ProfileValidationResponse:
    """Return a normalized profile without running recommendation logic."""
    summary = UserProfileSummary.model_validate(profile.model_dump())
    return ProfileValidationResponse(normalized_profile=summary)
