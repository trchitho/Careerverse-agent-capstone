"""Repository interfaces defining data access contracts."""

from __future__ import annotations

from typing import Any, Protocol

from app.models.saved_recommendation import SavedRecommendation


class CareerRepository(Protocol):
    """Protocol for career catalog data access."""

    def list_careers(self) -> list[dict[str, Any]]:
        """List all careers in the catalog."""
        ...

    def get_career_by_id(self, career_id: str) -> dict[str, Any]:
        """Retrieve a career by its ID. Raise ValueError if not found."""
        ...

    def search_careers(self, query: str, limit: int = 10) -> list[dict[str, Any]]:
        """Search careers matching search query."""
        ...


class SkillRepository(Protocol):
    """Protocol for skill metadata catalog data access."""

    def list_skills(self) -> list[dict[str, Any]]:
        """List all skills in the catalog."""
        ...

    def get_skill_by_name(self, skill_name: str) -> dict[str, Any]:
        """Retrieve skill metadata by name, ID or alias. Raise ValueError if not found."""
        ...


class RoadmapRepository(Protocol):
    """Protocol for study roadmap data access."""

    def list_roadmaps(self) -> dict[str, Any]:
        """List all roadmaps in the catalog."""
        ...

    def get_roadmap_by_career_id(self, career_id: str) -> dict[str, Any]:
        """Retrieve roadmap by career ID. Raise ValueError if not found."""
        ...


class SavedRecommendationRepository(Protocol):
    """Protocol for saved recommendation storage."""

    def save(self, item: SavedRecommendation) -> SavedRecommendation:
        """Save a new recommendation snapshot."""
        ...

    def list_by_session(self, session_id: str) -> list[SavedRecommendation]:
        """List recommendation snapshots saved for a specific session ID."""
        ...

    def get(self, item_id: str) -> SavedRecommendation | None:
        """Retrieve a specific saved recommendation snapshot by ID."""
        ...

    def clear(self) -> None:
        """Clear all stored recommendations (primarily for testing/session reset)."""
        ...
