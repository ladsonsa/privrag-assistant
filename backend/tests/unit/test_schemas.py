"""Unit tests for common and health API schema models."""

from backend.app.api.schemas.common import ErrorResponse
from backend.app.api.schemas.health import HealthResponse


def test_health_response_schema() -> None:
    """Tests that HealthResponse initializes correctly with valid attributes."""
    response = HealthResponse(status="ok")

    assert response.status == "ok"


def test_error_response_schema() -> None:
    """Tests that ErrorResponse initializes correctly with valid attributes."""
    response = ErrorResponse(detail="An error occurred")

    assert response.detail == "An error occurred"
