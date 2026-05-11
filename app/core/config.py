"""Runtime configuration loaded from environment variables."""

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    app_name: str = "Enterprise Underwriting AI Assistant"
    app_env: str = "local"
    log_level: str = "INFO"
    api_prefix: str = ""
    anthropic_api_key: str | None = None
    claude_model: str = "claude-3-5-sonnet-latest"
    claude_timeout_seconds: int = 30
    retrieval_min_score: float = 0.65
    trigger_rules_path: Path = Field(default=Path("config/trigger_rules.json"))

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    """Return cached settings instance."""
    return Settings()
