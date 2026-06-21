"""Saved recommendation model for session-safe storage."""

from __future__ import annotations

from pydantic import BaseModel


class SavedRecommendation(BaseModel):
    """Data transfer object for a saved recommendation snapshot."""

    id: str
    session_id: str
    created_at: str
    title: str
    career_id: str
    career_title: str
    score: float
    summary: str
    safety_notice: str
