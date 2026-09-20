"""Integration tests for application lifespan events and logging initialization."""

import logging

from fastapi.testclient import TestClient

from backend.app.main import app


def test_application_startup_configures_logging() -> None:
    """Tests that entering application lifespan configures the root logger."""
    with TestClient(app):
        root_logger = logging.getLogger()

        assert root_logger.level == logging.INFO
        assert len(root_logger.handlers) >= 1
