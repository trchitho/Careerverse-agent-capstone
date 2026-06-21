"""Environment-backed application settings."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings with safe local defaults."""

    app_name: str = "CareerVerse Agent"
    app_version: str = "0.1.0"
    environment: str = "development"
    model_name: str = "gemini-2.5-flash"
    google_api_key: str | None = None
    data_source: str = "json"
    database_url: str = ""
    enable_llm_explanations: bool = False
    saved_recommendation_store: str = "memory"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        protected_namespaces=("settings_",),
    )


@lru_cache
def get_settings() -> Settings:
    """Return a cached settings instance."""
    return Settings()
