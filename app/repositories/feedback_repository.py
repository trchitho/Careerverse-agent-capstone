"""In-memory feedback repository implementation."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Any


class InMemoryFeedbackRepository:
    """Ephemeral, process-local database for collecting recommendation feedback."""

    def __init__(self) -> None:
        self._records: list[dict[str, Any]] = []

    def save(
        self,
        session_id: str | None,
        career_id: str | None,
        career_title: str | None,
        rating: int,
        helpful: bool,
        comment: str | None,
        source: str = "web",
    ) -> dict[str, Any]:
        """Insert a safe feedback record into memory."""
        record_id = str(uuid.uuid4())
        created_at = datetime.now(UTC).isoformat()

        record = {
            "id": record_id,
            "created_at": created_at,
            "session_id": session_id,
            "career_id": career_id,
            "career_title": career_title,
            "rating": rating,
            "helpful": helpful,
            "comment": comment,
            "source": source,
        }
        self._records.append(record)
        return record

    def list_all(self) -> list[dict[str, Any]]:
        """Return all recorded feedback entries."""
        import copy
        return copy.deepcopy(self._records)

    def summary(self) -> dict[str, Any]:
        """Aggregate stored feedback records."""
        records = self._records
        if not records:
            return {
                "total_count": 0,
                "average_rating": 0.0,
                "helpful_count": 0,
                "not_helpful_count": 0,
            }

        ratings = [r["rating"] for r in records]
        avg_rating = sum(ratings) / len(ratings)
        helpful_count = sum(1 for r in records if r["helpful"])

        return {
            "total_count": len(records),
            "average_rating": round(avg_rating, 2),
            "helpful_count": helpful_count,
            "not_helpful_count": len(records) - helpful_count,
        }

    def clear(self) -> None:
        """Reset repository records for testing cycles."""
        self._records.clear()
