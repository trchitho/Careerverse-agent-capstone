"""Tests for API Versioning compatibility and structure."""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

PROFILE = {
    "name": "Demo User",
    "education": "Final-year IT student",
    "interests": ["AI", "web development"],
    "skills": ["Python", "React"],
    "career_goal": "Become an AI full-stack developer",
    "preferred_learning_style": "project_based",
    "language": "en",
    "experience_level": "university",
    "time_budget_hours_per_week": 8,
}


def test_legacy_endpoints_compatibility() -> None:
    """Verify that legacy endpoints still function properly."""
    res_root = client.get("/")
    assert res_root.status_code == 200
    assert "ok" in res_root.json()["status"]

    res_recommend = client.post("/recommend", json=PROFILE)
    assert res_recommend.status_code == 200
    assert "top_recommendations" in res_recommend.json()


def test_versioned_health_and_metadata() -> None:
    """Verify v1 health and metadata endpoints."""
    res_health = client.get("/api/v1/health")
    assert res_health.status_code == 200
    assert "ok" in res_health.json()["status"]

    res_meta = client.get("/api/v1/metadata")
    assert res_meta.status_code == 200
    assert "project" in res_meta.json()


def test_versioned_profiles_and_recommendations() -> None:
    """Verify v1 profile validate and recommend endpoints."""
    res_val = client.post("/api/v1/profiles/validate", json=PROFILE)
    assert res_val.status_code == 200
    assert "normalized_profile" in res_val.json()

    res_rec = client.post("/api/v1/recommend", json=PROFILE)
    assert res_rec.status_code == 200
    assert "top_recommendations" in res_rec.json()

    legacy_rec = client.post("/recommend", json=PROFILE).json()
    assert res_rec.json().keys() == legacy_rec.keys()


def test_versioned_mcp_endpoints() -> None:
    """Verify v1 MCP resource endpoints."""
    res_tools = client.get("/api/v1/tools")
    assert res_tools.status_code == 200
    assert "tools" in res_tools.json()

    res_careers = client.get("/api/v1/mcp/careers?limit=5")
    assert res_careers.status_code == 200

    res_skills = client.get("/api/v1/mcp/skills?limit=5")
    assert res_skills.status_code == 200

    res_search_c = client.get("/api/v1/mcp/search/careers?q=AI")
    assert res_search_c.status_code == 200

    res_search_s = client.get("/api/v1/mcp/search/skills?q=Python")
    assert res_search_s.status_code == 200

    res_safety = client.post("/api/v1/safety/validate-profile", json=PROFILE)
    assert res_safety.status_code == 200
    assert "is_safe" in res_safety.json()
