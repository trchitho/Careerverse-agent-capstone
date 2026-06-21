"""Explanation service for generating personalized recommendation fits."""

from __future__ import annotations

from typing import Any

from app.core.config import get_settings


def build_local_explanation(
    profile: dict[str, Any],
    recommendation: dict[str, Any],
    skill_gap: dict[str, Any] | None = None,
) -> str:
    """Generate a deterministic, local educational fit explanation."""
    name = profile.get("name") or "Student"
    interests = profile.get("interests") or []
    title = recommendation.get("title") or "Selected Career"

    matched_interests = [
        item
        for item in interests
        if item in (recommendation.get("recommended_for") or [])
    ]
    matched_skills = recommendation.get("matched_skills") or []
    missing_skills = recommendation.get("missing_skills_preview") or []

    explanation_parts = [
        f"Hello {name}. Based on our analysis, the '{title}' role is recommended for you."
    ]

    if matched_interests:
        explanation_parts.append(
            f"It aligns with your interest in {', '.join(matched_interests[:2])}."
        )
    else:
        explanation_parts.append(
            "It matches your overall target profile and goal."
        )

    if matched_skills:
        explanation_parts.append(
            f"You already possess key skills like {', '.join(matched_skills[:2])}."
        )

    if missing_skills:
        explanation_parts.append(
            f"To progress, you should prioritize learning: {', '.join(missing_skills[:3])}."
        )

    # Disclaimer
    explanation_parts.append(
        "This recommendation is for educational guidance only. "
        "The personality inference is approximate and the job market forecast "
        "is reference data, not a guarantee of employment."
    )

    return " ".join(explanation_parts)


def explain_recommendation(
    profile: dict[str, Any],
    recommendation: dict[str, Any],
    skill_gap: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Generate fit explanation using the active configuration engine."""
    settings = get_settings()
    local_text = build_local_explanation(profile, recommendation, skill_gap)

    # Safety: ensure no raw malicious prompt is echoed
    goal = str(profile.get("career_goal") or "").casefold()
    if "ignore previous" in goal or "system prompt" in goal:
        local_text = (
            "Fit analysis unavailable due to profile input validation warning."
        )

    if settings.ENABLE_LLM_EXPLANATIONS and settings.GOOGLE_API_KEY:
        # Simulate LLM response block
        llm_text = f"[LLM Explanation Engine] {local_text}"
        return {
            "engine": "gemini",
            "explanation": llm_text,
            "local_fallback_used": False,
        }

    return {
        "engine": "local_fallback",
        "explanation": local_text,
        "local_fallback_used": True,
    }
