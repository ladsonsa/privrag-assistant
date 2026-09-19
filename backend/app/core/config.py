"""Application settings management module.

Loads environment variables using Pydantic BaseSettings and provides
a cached accessor for configuration instances.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings schema loaded from environment variables."""

    app_name: str = "PrivRAG Assistant"
    app_env: str = "development"
    debug: bool = False
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Retrieves cached application settings instance.

    Returns:
        Settings: Singleton instance containing runtime settings.
    """
    return Settings()
