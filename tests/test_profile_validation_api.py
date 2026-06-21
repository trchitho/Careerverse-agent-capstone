"""API tests for profile validation and normalization."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def valid_payload() -> dict[str, object]:
    return {
        "name": "  Tho  ",
        "education": "Final-year IT student",
        "interests": ["AI", " ai ", "web   development"],
        "skills": ["Python", " python ", "React", "SQL"],
        "career_goal": "Become an AI full-stack developer",
    }


def test_validate_profile_returns_normalized_response() -> None:
    response = client.post("/profiles/validate", json=valid_payload())

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "valid"
    assert body["normalized_profile"]["name"] == "Tho"
    assert body["normalized_profile"]["interests"] == ["AI", "web development"]
    assert body["normalized_profile"]["skills"] == ["Python", "React", "SQL"]
    assert body["warnings"] == []


def test_validate_profile_rejects_invalid_payload() -> None:
    response = client.post(
        "/profiles/validate",
        json=valid_payload() | {"language": "unsupported"},
    )

    assert response.status_code == 422


def test_existing_health_endpoint_still_works() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_existing_metadata_endpoint_reports_stage() -> None:
    response = client.get("/metadata")

    assert response.status_code == 200
    assert response.json()["project"] == "CareerVerse Agent"
    assert response.json()["current_stage"] == "local_evaluation_pipeline"
