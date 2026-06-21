"""Service for managing user session saved recommendations."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Any

from app.models.saved_recommendation import SavedRecommendation
from app.repositories.session_repository import (
    InMemorySavedRecommendationRepository,
)

_session_repo = InMemorySavedRecommendationRepository()


def create_saved_recommendation(
    session_id: str,
    recommendation_response: dict[str, Any],
) -> SavedRecommendation:
    """Extract safe summary fields and save a snapshot to session repository."""
    if not session_id or not session_id.strip():
        raise ValueError("session_id must not be blank")

    top_recs = recommendation_response.get("top_recommendations") or []
    if not top_recs:
        raise ValueError("No recommendations found in response to save.")

    top_rec = top_recs[0]
    career_id = str(top_rec.get("career_id") or "")
    career_title = str(top_rec.get("title") or "")
    score = float(top_rec.get("score") or 0.0)

    reasons = top_rec.get("matched_reasons") or []
    summary = " ".join(reasons) if reasons else "No summary available."

    item_id = str(uuid.uuid4())
    created_at = datetime.now(UTC).isoformat()

    saved_item = SavedRecommendation(
        id=item_id,
        session_id=session_id.strip(),
        created_at=created_at,
        title=f"Saved recommendation for {career_title}",
        career_id=career_id,
        career_title=career_title,
        score=score,
        summary=summary,
        safety_notice=str(recommendation_response.get("safety_notice") or ""),
    )

    _session_repo.save(saved_item)
    return saved_item


def list_saved_recommendations(session_id: str) -> list[SavedRecommendation]:
    """Retrieve saved recommendations for a given session ID."""
    if not session_id or not session_id.strip():
        raise ValueError("session_id must not be blank")
    return _session_repo.list_by_session(session_id)
