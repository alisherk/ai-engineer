from functools import lru_cache

from pydantic import ConfigDict
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    text_embedding_model: str = "text-embedding-3-small"
    pushover_user: str = ""
    pushover_token: str = ""
    pushover_api: str = "https://api.pushover.net/1/messages.json"

    model_config = ConfigDict(env_file=".env", case_sensitive=False, extra="ignore")


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
