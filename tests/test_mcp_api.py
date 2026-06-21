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


def test_career_detail_skills_and_roadmap_endpoints() -> None:
    career_id = client.get("/mcp/careers?limit=1").json()["items"][0]["career_id"]

    detail = client.get(f"/mcp/careers/{career_id}")
    skills = client.get(f"/mcp/careers/{career_id}/skills")
    roadmap = client.get(f"/mcp/careers/{career_id}/roadmap")

    assert detail.status_code == 200
    assert skills.status_code == 200
    assert roadmap.status_code == 200
    assert detail.json()["id"] == career_id
    assert skills.json()["required_skills"]
    assert roadmap.json()["career_id"] == career_id


def test_unknown_career_resources_return_404() -> None:
    assert client.get("/mcp/careers/not_real_id").status_code == 404
    assert client.get("/mcp/careers/not_real_id/skills").status_code == 404
    assert client.get("/mcp/careers/not_real_id/roadmap").status_code == 404


def test_skill_listing_and_detail_endpoints() -> None:
    listing = client.get("/mcp/skills?limit=5")

    assert listing.status_code == 200
    assert listing.json()["count"] == 5
    skill = listing.json()["items"][0]
    detail = client.get(f"/mcp/skills/{skill['id']}")
    assert detail.status_code == 200
    assert detail.json()["name"] == skill["name"]


def test_unknown_skill_returns_404() -> None:
    assert client.get("/mcp/skills/not_real_skill").status_code == 404


def test_career_and_skill_search_endpoints() -> None:
    careers = client.get("/mcp/search/careers?q=AI")
    skills = client.get("/mcp/search/skills?q=Python")

    assert careers.status_code == 200
    assert careers.json()["items"]
    assert skills.status_code == 200
    assert skills.json()["items"]
    assert client.get("/mcp/search/careers?q=").status_code == 422


def test_existing_endpoints_remain_available() -> None:
    assert client.get("/").status_code == 200
    assert client.get("/metadata").status_code == 200
    assert client.post("/profiles/validate", json=sample_profile()).status_code == 200
    assert client.post("/recommend", json=sample_profile()).status_code == 200
