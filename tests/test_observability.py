"""Unit tests for liveness/readiness health check endpoints and request ID tracking."""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_live_endpoint() -> None:
    """Verify live check responds with 200 and liveness status."""
    res = client.get("/api/v1/health/live")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"
    assert "X-Request-ID" in res.headers


def test_health_ready_endpoint() -> None:
    """Verify readiness check responds with 200 and readiness status."""
    res = client.get("/api/v1/health/ready")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"
    assert "X-Request-ID" in res.headers


def test_request_id_middleware_preserves_header() -> None:
    """Verify incoming X-Request-ID is echoed in response headers."""
    req_id = "test-custom-id-12345"
    res = client.get("/api/v1/health/live", headers={"X-Request-ID": req_id})
    assert res.status_code == 200
    assert res.headers["X-Request-ID"] == req_id


def test_request_id_middleware_generates_header() -> None:
    """Verify unique request ID is generated when X-Request-ID is missing."""
    res1 = client.get("/api/v1/health/live")
    res2 = client.get("/api/v1/health/live")
    assert res1.headers["X-Request-ID"] != res2.headers["X-Request-ID"]


def test_legacy_health_check_endpoint() -> None:
    """Verify old legacy root health path remains compatible."""
    res = client.get("/")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"
