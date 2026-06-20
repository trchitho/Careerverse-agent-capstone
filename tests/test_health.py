"""API bootstrap endpoint tests."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "message": "CareerVerse Agent is running.",
    }


def test_metadata_endpoint() -> None:
    response = client.get("/metadata")
    body = response.json()

    assert response.status_code == 200
    assert body["project"] == "CareerVerse Agent"
    assert body["track"] == "Agents for Good"
    assert body["course_concepts_demonstrated"]
