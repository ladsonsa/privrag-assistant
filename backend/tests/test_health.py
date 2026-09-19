"""Integration tests for application health check and utility endpoints."""

from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_health_check() -> None:
    """Tests that /health returns HTTP 200 and expected status payload."""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
