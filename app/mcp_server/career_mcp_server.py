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
