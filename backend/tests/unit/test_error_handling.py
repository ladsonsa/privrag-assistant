"""Integration tests for application error handling and default routes."""

from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_not_found_error_returns_standard_response() -> None:
    """Tests that accessing an unmapped route returns HTTP 404 with ErrorResponse."""
    response = client.get("/non-existent-route")

    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}
