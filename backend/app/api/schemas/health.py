"""Health check schema definition module."""

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Schema representing the health status response payload."""

    status: str
