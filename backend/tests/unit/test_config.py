"""Unit tests for core application settings and environment overrides."""

import _pytest.monkeypatch

from backend.app.core.config import Settings


def test_settings_use_defaults() -> None:
    """Tests that Settings initializes with expected default values."""
    settings = Settings(_env_file=None)

    assert settings.app_name == "PrivRAG Assistant"
    assert settings.app_env == "development"
    assert settings.debug is False
    assert settings.log_level == "INFO"


def test_settings_load_environment_variables(
    monkeypatch: _pytest.monkeypatch.MonkeyPatch,
) -> None:
    """Tests that environment variables correctly override default settings."""
    monkeypatch.setenv("APP_NAME", "Test Application")
    monkeypatch.setenv("APP_ENV", "testing")
    monkeypatch.setenv("DEBUG", "true")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")

    settings = Settings(_env_file=None)

    assert settings.app_name == "Test Application"
    assert settings.app_env == "testing"
    assert settings.debug is True
    assert settings.log_level == "DEBUG"
