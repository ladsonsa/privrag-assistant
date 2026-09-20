"""PrivRAG Assistant FastAPI application entry point module.

Configures application lifecycle handlers, logging initialization, custom exception
handlers, and exposes core operational endpoints.
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from backend.app.api.schemas.common import ErrorResponse
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


@app.exception_handler(HTTPException)
async def http_exception_handler(
    _: Request,
    exc: HTTPException,
) -> JSONResponse:
    """Handles HTTPExceptions and formats responses using ErrorResponse schema.

    Args:
        _: Incoming HTTP request object.
        exc: Raised HTTPException instance.

    Returns:
        JSONResponse: Formatted JSON response with ErrorResponse payload.
    """
    error_response = ErrorResponse(detail=str(exc.detail))

    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.model_dump(),
        headers=exc.headers,
    )


@app.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    """Health check endpoint to verify service availability.

    Returns:
        HealthResponse: Schema instance containing the operational status.
    """
    return HealthResponse(status="ok")
