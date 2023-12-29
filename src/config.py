from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    env_name: str = "Local"
    enable_json_logs: bool = True
    log_level: str = "INFO"

    db_url: str = "sqlite:///:memory:"

    model_config = SettingsConfigDict(extra="ignore", env_file=".env")

    # auth
    access_token_expire_minutes: int = 60
    secret_key: str = "123"
    algorithm: str = "HS256"

    datetime_format: str = "%m-%Y-%dT%H:%M:%S"


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    print(f"Loading settings for: {settings.env_name}")
    return settings
