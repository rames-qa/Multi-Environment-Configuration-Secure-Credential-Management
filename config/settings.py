
import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    env: str = Field(default="dev", validation_alias="TEST_ENV")

    base_url: str
    auth_url: str = ""

    client_id: str = ""
    client_secret: str = ""

    timeout: float = 10.0
    max_retries: int = 2

    model_config = SettingsConfigDict(
        env_file=None,
        env_file_encoding="utf-8",
        extra="ignore"
    )


def load_settings():
    environment = os.getenv("TEST_ENV", "dev").lower()

    return Settings(
        _env_file=f"config/{environment}.env"
    )


settings = load_settings()
