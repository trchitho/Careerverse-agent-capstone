"""MCP-style local career resource server for the Kaggle Capstone."""

from copy import deepcopy
from typing import Any

from app.agents import RoadmapAgent
from app.tools.career_tools import (
    build_search_text,
    load_careers,
    load_skills,
    normalize_text,
    tokenize_text,
)

MAX_PAGE_SIZE = 100


def _validate_pagination(limit: int, offset: int) -> None:
    """Validate shared pagination bounds."""
    if not 1 <= limit <= MAX_PAGE_SIZE:
        raise ValueError("limit must be between 1 and 100")
    if offset < 0:
        raise ValueError("offset must be greater than or equal to 0")


def _paginate(items: list[dict[str, Any]], limit: int, offset: int) -> dict[str, Any]:
    """Return a copied, stable paginated resource response."""
    _validate_pagination(limit, offset)
    page = deepcopy(items[offset : offset + limit])
    return {
        "items": page,
        "count": len(page),
        "total": len(items),
        "limit": limit,
        "offset": offset,
    }


class CareerMCPServer:
    """Expose local career knowledge as machine-readable tool resources."""

    def __init__(self, roadmap_agent: RoadmapAgent | None = None) -> None:
        self.roadmap_agent = roadmap_agent or RoadmapAgent()

    @staticmethod
    def _career_summary(career: dict[str, Any]) -> dict[str, Any]:
        """Return the lightweight career listing representation."""
        return {
            "career_id": career["id"],
            "title": career["title"],
            "family": career.get("family"),
            "level": career.get("level"),
            "description": career["description"],
            "market_relevance": deepcopy(career.get("market_relevance")),
        }

    @staticmethod
    def _matches_filter(value: object, expected: str | None) -> bool:
        """Apply an optional case-insensitive exact filter."""
        if expected is None:
            return True
        normalized = normalize_text(expected)
        if not normalized:
            raise ValueError("filter values must not be blank")
        return normalize_text(str(value or "")) == normalized

    def list_available_careers(
        self,
        family: str | None = None,
        level: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> dict[str, Any]:
        """List lightweight career resources with optional filters."""
        filtered = [
            self._career_summary(career)
            for career in load_careers()
            if self._matches_filter(career.get("family"), family)
            and self._matches_filter(career.get("level"), level)
        ]
        filtered.sort(
            key=lambda item: (
                normalize_text(str(item["title"])),
                normalize_text(str(item["career_id"])),
            )
        )
        return _paginate(filtered, limit, offset)

    def get_career_by_id(self, career_id: str) -> dict[str, Any]:
        """Return one full career resource by normalized identifier."""
        normalized = normalize_text(career_id)
        if not normalized:
            raise ValueError("career_id must not be blank")
        for career in load_careers():
            if normalize_text(str(career["id"])) == normalized:
                return deepcopy(career)
        raise ValueError(f"Career not found: {career_id}")
