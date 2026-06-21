"""MCP resource and tool catalog routes for version 1 API."""

from __future__ import annotations

from fastapi import APIRouter, Query

from app.core.exceptions import ResourceNotFoundError
from app.mcp_server import CareerMCPServer

router = APIRouter(tags=["MCP Tools"])
mcp_server = CareerMCPServer()


@router.get("/tools")
def tool_catalog() -> dict[str, object]:
    """Return discoverable MCP-style local tool definitions."""
    tools = mcp_server.list_tool_catalog()
    return {"tools": tools, "count": len(tools)}


@router.get("/mcp/careers")
def mcp_careers(
    family: str | None = Query(default=None, min_length=1),
    level: str | None = Query(default=None, min_length=1),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> dict[str, object]:
    """List paginated career resources."""
    return mcp_server.list_available_careers(family, level, limit, offset)


@router.get("/mcp/careers/{career_id}")
def mcp_career(career_id: str) -> dict[str, object]:
    """Return one career resource or a safe 404."""
    try:
        return mcp_server.get_career_by_id(career_id)
    except ValueError as error:
        raise ResourceNotFoundError(str(error)) from error


@router.get("/mcp/careers/{career_id}/skills")
def mcp_career_skills(career_id: str) -> dict[str, object]:
    """Return required and optional career skill resources."""
    try:
        return mcp_server.get_required_skills(career_id)
    except ValueError as error:
        raise ResourceNotFoundError(str(error)) from error


@router.get("/mcp/careers/{career_id}/roadmap")
def mcp_career_roadmap(career_id: str) -> dict[str, object]:
    """Return one stored roadmap resource."""
    try:
        return mcp_server.get_roadmap_for_career(career_id)
    except ValueError as error:
        raise ResourceNotFoundError(str(error)) from error


@router.get("/mcp/skills")
def mcp_skills(
    category: str | None = Query(default=None, min_length=1),
    level: str | None = Query(default=None, min_length=1),
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> dict[str, object]:
    """List paginated skill resources."""
    return mcp_server.list_available_skills(category, level, limit, offset)


@router.get("/mcp/skills/{skill_name}")
def mcp_skill(skill_name: str) -> dict[str, object]:
    """Return one skill resource or a safe 404."""
    try:
        return mcp_server.get_skill_metadata(skill_name)
    except ValueError as error:
        raise ResourceNotFoundError(str(error)) from error


@router.get("/mcp/search/careers")
def mcp_search_careers(
    q: str = Query(min_length=1),
    limit: int = Query(default=10, ge=1, le=50),
    offset: int = Query(default=0, ge=0),
) -> dict[str, object]:
    """Search career resources by interest text."""
    try:
        return mcp_server.search_careers_by_interest(q, limit, offset)
    except ValueError as error:
        raise ResourceNotFoundError(str(error)) from error


@router.get("/mcp/search/skills")
def mcp_search_skills(
    q: str = Query(min_length=1),
    category: str | None = Query(default=None, min_length=1),
    level: str | None = Query(default=None, min_length=1),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> dict[str, object]:
    """Search skill resources by text."""
    try:
        return mcp_server.search_skills(q, category, level, limit, offset)
    except ValueError as error:
        raise ResourceNotFoundError(str(error)) from error
