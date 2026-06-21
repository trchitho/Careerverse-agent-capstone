"""Version 1 API routers package."""

from __future__ import annotations

from fastapi import APIRouter

from app.api.v1.health import router as health_router
from app.api.v1.mcp import router as mcp_router
from app.api.v1.profiles import router as profiles_router
from app.api.v1.recommendations import router as recommendations_router
from app.api.v1.safety import router as safety_router

v1_router = APIRouter()
v1_router.include_router(health_router)
v1_router.include_router(profiles_router)
v1_router.include_router(recommendations_router)
v1_router.include_router(mcp_router)
v1_router.include_router(safety_router)
