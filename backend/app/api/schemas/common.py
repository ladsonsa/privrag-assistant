"""Error response schema definition module."""

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """Schema representing an API error response payload."""

    detail: str
