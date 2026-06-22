"""Full project functional integration regression tests."""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_legacy_and_versioned_health_and_metadata() -> None:
    # 1. Health checks
    res = client.get("/")
    assert res.status_code == 200
    assert "status" in res.json()
    
    res = client.get("/api/v1/health/live")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"
    
    res = client.get("/api/v1/health/ready")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"
    
    # 2. Metadata checks
    res = client.get("/metadata")
    assert res.status_code == 200
    assert "version" in res.json()
    
    res = client.get("/api/v1/health/live")
    assert res.status_code == 200


def test_profile_validation_endpoint() -> None:
    # Valid profile
    payload = {
        "name": "Alex",
        "education": "IT graduate",
        "interests": ["AI"],
        "skills": ["Python"],
        "career_goal": "Become an AI researcher"
    }
    res = client.post("/profiles/validate", json=payload)
    assert res.status_code == 200
    assert res.json()["normalized_profile"]["name"] == "Alex"
    
    # Invalid profile
    bad_payload = {
        "name": "",
        "education": "IT graduate",
        "interests": [],
        "skills": [],
        "career_goal": ""
    }
    res = client.post("/profiles/validate", json=bad_payload)
    assert res.status_code == 422


def test_recommendation_pipeline_and_response_fields() -> None:
    payload = {
        "name": "Jane",
        "education": "IT student",
        "interests": ["Cybersecurity"],
        "skills": ["Linux"],
        "career_goal": "Work in threat analysis"
    }
    # legacy endpoint
    res = client.post("/recommend", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "top_recommendations" in data
    assert "safety_notice" in data
    
    # versioned endpoint with top_k bounds
    res = client.post("/api/v1/recommend?top_k=2", json=payload)
    assert res.status_code == 200
    data_v1 = res.json()
    assert len(data_v1["top_recommendations"]) <= 2
    assert "readiness_score" in data_v1["skill_gap"]
    assert "personalized_roadmap" in data_v1


def test_saved_recommendations_workflow() -> None:
    save_payload = {
        "session_id": "session-123",
        "recommendation_response": {
            "top_recommendations": [
                {
                    "career_id": "cloud-engineer",
                    "title": "Cloud Engineer",
                    "score": 85.0,
                    "matched_reasons": ["Has cloud interest"]
                }
            ],
            "safety_notice": "Disclaimer notice"
        }
    }
    res = client.post("/api/v1/recommendations/save", json=save_payload)
    assert res.status_code == 200
    assert res.json()["session_id"] == "session-123"
    
    res = client.get("/api/v1/recommendations/saved/session-123")
    assert res.status_code == 200
    assert len(res.json()) >= 1


def test_feedback_and_metrics_endpoints() -> None:
    feedback_payload = {
        "rating": 5,
        "helpful": True,
        "comment": "Outstanding recommendations dashboard."
    }
    res = client.post("/api/v1/feedback/recommendation", json=feedback_payload)
    assert res.status_code == 201
    
    res = client.get("/api/v1/feedback/summary")
    assert res.status_code == 200
    assert "average_rating" in res.json()


def test_mcp_discovery_and_resources() -> None:
    res = client.get("/tools")
    assert res.status_code == 200
    
    res = client.get("/api/v1/tools")
    assert res.status_code == 200
    
    res = client.get("/mcp/careers")
    assert res.status_code == 200
    
    res = client.get("/mcp/skills")
    assert res.status_code == 200
