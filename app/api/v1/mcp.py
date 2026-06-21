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
