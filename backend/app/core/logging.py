"""Logging configuration module for application-wide structured log management."""

import logging
from logging.config import dictConfig

from backend.app.core.config import get_settings


def configure_logging() -> None:
    """Configures application-wide logging dictionary based on core settings."""
    settings = get_settings()

    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": ("%(asctime)s | %(levelname)s | %(name)s | %(message)s"),
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                    "stream": "ext://sys.stdout",
                },
            },
            "root": {
                "level": settings.log_level,
                "handlers": ["console"],
            },
        }
    )


def get_logger(name: str) -> logging.Logger:
    """Retrieves a named logger instance.

    Args:
        name: Name identifier for the logger instance.

    Returns:
        logging.Logger: Configured standard logging instance.
    """
    return logging.getLogger(name)
