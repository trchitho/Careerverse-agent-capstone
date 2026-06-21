"""API tests for MCP-style career resource endpoints."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def sample_profile() -> dict[str, object]:
    return {
        "name": "Demo User",
        "education": "IT student",
        "interests": ["AI"],
        "skills": ["Python"],
        "career_goal": "Build AI products",
    }


def test_tool_catalog_endpoint() -> None:
    response = client.get("/tools")

    assert response.status_code == 200
    assert response.json()["count"] == 8
    assert response.json()["tools"]


def test_career_listing_endpoint_and_bounds() -> None:
    response = client.get("/mcp/careers?limit=5")

    assert response.status_code == 200
    assert response.json()["count"] == 5
    assert client.get("/mcp/careers?limit=0").status_code == 422
