from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "LuminaLib"
    database_url: str
    jwt_secret: str
    jwt_algorithm: str
    access_token_expire_minutes: int

    model_config = SettingsConfigDict(
        env_file=".env",
        extra = "ignore",
    )

@lru_cache()
def get_settings():
    return Settings()
