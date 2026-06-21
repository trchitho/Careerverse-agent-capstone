"""Session-based in-memory repository for saved recommendations."""

from __future__ import annotations

from app.models.saved_recommendation import SavedRecommendation


class InMemorySavedRecommendationRepository:
    """Process-local in-memory storage for saved recommendations."""

    def __init__(self) -> None:
        # Key: saved recommendation ID, Value: SavedRecommendation
        self._store: dict[str, SavedRecommendation] = {}

    def save(self, item: SavedRecommendation) -> SavedRecommendation:
        """Save a new recommendation snapshot."""
        if not item.id or not item.id.strip():
            raise ValueError("SavedRecommendation id must not be blank")
        if not item.session_id or not item.session_id.strip():
            raise ValueError("SavedRecommendation session_id must not be blank")
        self._store[item.id] = item
        return item

    def list_by_session(self, session_id: str) -> list[SavedRecommendation]:
        """List recommendation snapshots saved for a specific session ID."""
        normalized = session_id.strip()
        if not normalized:
            raise ValueError("session_id must not be blank")
        return [
            item
            for item in self._store.values()
            if item.session_id == normalized
        ]

    def get(self, item_id: str) -> SavedRecommendation | None:
        """Retrieve a specific saved recommendation snapshot by ID."""
        normalized = item_id.strip()
        if not normalized:
            raise ValueError("item_id must not be blank")
        return self._store.get(normalized)

    def clear(self) -> None:
        """Clear all stored recommendations."""
        self._store.clear()
