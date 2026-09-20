"""PrivRAG Assistant FastAPI application entry point module.

Configures application lifecycle handlers, logging initialization, and exposes
core operational endpoints.
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.app.api.schemas.health import HealthResponse
from backend.app.core.logging import configure_logging


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Lifespan context manager for handling startup and shutdown events."""
    configure_logging()
    yield


app = FastAPI(
    title="PrivRAG Assistant",
    lifespan=lifespan,
)


@app.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    """Health check endpoint to verify service availability.

    Returns:
        HealthResponse: Schema instance containing the operational status.
    """
    return HealthResponse(status="ok")
