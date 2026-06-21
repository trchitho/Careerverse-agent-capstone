"""Safety and data redaction routes for version 1 API."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from app.schemas import UserProfileRequest
from app.tools.safety_tools import validate_profile_safety

router = APIRouter(tags=["Safety"])


@router.post("/safety/validate-profile")
def validate_profile_safety_route(profile: UserProfileRequest) -> dict[str, Any]:
    """Inspect profile text for overrides and redact sensitive data."""
    safety_result = validate_profile_safety(profile)
    return {
        "is_safe": safety_result["is_safe"],
        "risk_level": safety_result["risk_level"],
        "issues_count": len(safety_result["issues"]),
        "issues": safety_result["issues"],
    }
