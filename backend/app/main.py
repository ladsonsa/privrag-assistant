"""PrivRAG Assistant FastAPI application entry point module."""

from fastapi import FastAPI

from backend.app.api.schemas.health import HealthResponse

app = FastAPI(title="PrivRAG Assistant")


@app.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    """Health check endpoint to verify service availability.

    Returns:
        HealthResponse: Schema instance containing the operational status.
    """
    return HealthResponse(status="ok")
