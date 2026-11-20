import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    env: str = os.getenv("TEST_ENV", "dev")
    base_url: str
    auth_url: str = ""
    client_id: str = ""
    client_secret: str = ""
    timeout: float = 10.0
    max_retries: int = 2

    model_config = SettingsConfigDict(
        env_file=(f"config/{os.getenv('TEST_ENV', 'dev')}.env", ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
