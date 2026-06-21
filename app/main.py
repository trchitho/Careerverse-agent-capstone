"""FastAPI entrypoint for the CareerVerse Agent service."""

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.agents import CareerAdvisorAgent
from app.core.config import get_settings
from app.core.constants import (
    COURSE_CONCEPTS,
    KAGGLE_TRACK,
    PROJECT_DESCRIPTION,
    PROJECT_NAME,
    PROJECT_VERSION,
)
from app.mcp_server import CareerMCPServer
from app.schemas import (
    AgentRecommendationResponse,
    ProfileValidationResponse,
    UserProfileRequest,
    UserProfileSummary,
)
from app.tools.safety_tools import get_safety_notice, validate_profile_safety

settings = get_settings()
career_advisor = CareerAdvisorAgent()
mcp_server = CareerMCPServer()
app = FastAPI(
    title=settings.app_name,
    description=PROJECT_DESCRIPTION,
    version=settings.app_version,
)


@app.exception_handler(RequestValidationError)
async def safe_request_validation_error(
    request: Request,
    error: RequestValidationError,
) -> JSONResponse:
    """Map schema-detected injection on /recommend to a non-echoing safe error."""
    injection_error = any(
        "disallowed instruction pattern" in str(item.get("msg", ""))
        for item in error.errors()
    )
    if request.url.path == "/recommend" and injection_error:
        return JSONResponse(
            status_code=400,
            content={
                "detail": {
                    "error": "unsafe_profile",
                    "message": "The profile contains unsafe content and cannot be processed.",
                    "risk_level": "high",
                }
            },
        )
    return await request_validation_exception_handler(request, error)


@app.get("/")
def health_check() -> dict[str, str]:
    """Return the public service health state."""
    return {"status": "ok", "message": "CareerVerse Agent is running."}


@app.get("/metadata")
def metadata() -> dict[str, object]:
    """Return public project and runtime metadata."""
    return {
        "project": PROJECT_NAME,
        "description": PROJECT_DESCRIPTION,
        "version": PROJECT_VERSION,
        "track": KAGGLE_TRACK,
        "environment": settings.environment,
        "current_stage": "local_evaluation_pipeline",
        "course_concepts_demonstrated": COURSE_CONCEPTS,
    }


@app.post("/profiles/validate", response_model=ProfileValidationResponse)
def validate_profile(profile: UserProfileRequest) -> ProfileValidationResponse:
    """Return a normalized profile without running recommendation logic."""
    summary = UserProfileSummary.model_validate(profile.model_dump())
    return ProfileValidationResponse(normalized_profile=summary)


@app.post("/recommend", response_model=AgentRecommendationResponse)
def recommend(
    profile: UserProfileRequest,
    top_k: int = Query(default=3, ge=1, le=10),
) -> AgentRecommendationResponse:
    """Run the deterministic multi-agent career guidance workflow."""
    safety_result = validate_profile_safety(profile)
    if not safety_result["is_safe"]:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "unsafe_profile",
                "message": safety_result["safe_message"],
                "risk_level": safety_result["risk_level"],
            },
        )
    try:
        payload = career_advisor.run(safety_result["redacted_profile"], top_k=top_k)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    payload["safety_notice"] = get_safety_notice()
    return AgentRecommendationResponse.model_validate(payload)


@app.get("/tools")
def tool_catalog() -> dict[str, object]:
    """Return discoverable MCP-style local tool definitions."""
    tools = mcp_server.list_tool_catalog()
    return {"tools": tools, "count": len(tools)}


@app.get("/mcp/careers")
def mcp_careers(
    family: str | None = Query(default=None, min_length=1),
    level: str | None = Query(default=None, min_length=1),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> dict[str, object]:
    """List paginated career resources."""
    return mcp_server.list_available_careers(family, level, limit, offset)


@app.get("/mcp/careers/{career_id}")
def mcp_career(career_id: str) -> dict[str, object]:
    """Return one career resource or a safe 404."""
    try:
        return mcp_server.get_career_by_id(career_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@app.get("/mcp/careers/{career_id}/skills")
def mcp_career_skills(career_id: str) -> dict[str, object]:
    """Return required and optional career skill resources."""
    try:
        return mcp_server.get_required_skills(career_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@app.get("/mcp/careers/{career_id}/roadmap")
def mcp_career_roadmap(career_id: str) -> dict[str, object]:
    """Return one stored roadmap resource."""
    try:
        return mcp_server.get_roadmap_for_career(career_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@app.get("/mcp/skills")
def mcp_skills(
    category: str | None = Query(default=None, min_length=1),
    level: str | None = Query(default=None, min_length=1),
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> dict[str, object]:
    """List paginated skill resources."""
    return mcp_server.list_available_skills(category, level, limit, offset)


@app.get("/mcp/skills/{skill_name}")
def mcp_skill(skill_name: str) -> dict[str, object]:
    """Return one skill resource or a safe 404."""
    try:
        return mcp_server.get_skill_metadata(skill_name)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@app.get("/mcp/search/careers")
def mcp_search_careers(
    q: str = Query(min_length=1),
    limit: int = Query(default=10, ge=1, le=50),
    offset: int = Query(default=0, ge=0),
) -> dict[str, object]:
    """Search career resources by interest text."""
    try:
        return mcp_server.search_careers_by_interest(q, limit, offset)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.get("/mcp/search/skills")
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
        raise HTTPException(status_code=400, detail=str(error)) from error
