"""PrivRAG Assistant FastAPI application module.

Provides entry points and health check endpoints for application monitoring and status.
"""

from fastapi import FastAPI

app = FastAPI(title="PrivRAG Assistant")


@app.get("/health")
def health_check() -> dict[str, str]:
    """Health check endpoint to verify service availability.

    Returns:
        dict[str, str]: Status payload indicating application operational state.
    """
    return {"status": "ok"}
