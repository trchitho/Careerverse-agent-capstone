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
