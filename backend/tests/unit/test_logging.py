"""Unit tests for the application logging configuration and logger factory."""

import logging

from backend.app.core.logging import configure_logging, get_logger


def test_get_logger_returns_named_logger() -> None:
    """Tests that get_logger returns a Logger instance with the expected name."""
    logger = get_logger("test_module")

    assert isinstance(logger, logging.Logger)
    assert logger.name == "test_module"


def test_configure_logging_sets_root_level() -> None:
    """Tests that configure_logging sets root logger level and attaches handlers."""
    configure_logging()

    root_logger = logging.getLogger()

    assert root_logger.level == logging.INFO
    assert len(root_logger.handlers) >= 1
