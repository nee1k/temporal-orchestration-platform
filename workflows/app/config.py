from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyUrl, Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="APP_", env_file=None, case_sensitive=False)

    temporal_address: str = Field(default="localhost:7233", validation_alias="TEMPORAL_ADDRESS")
    task_queue: str = Field(default="doc-pipeline")

    # External services (example)
    s3_endpoint_url: str | None = None
    notifications_topic: str | None = None

    log_level: str = Field(default="INFO")


settings = Settings()
