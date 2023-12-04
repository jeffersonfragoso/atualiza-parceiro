from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    env_name: str = "Local"
    db_url: str = "sqlite:///:memory:"

    model_config = SettingsConfigDict(extra="ignore", env_file=".env")


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    print(f"Loading settings for: {settings.env_name}")
    return settings
