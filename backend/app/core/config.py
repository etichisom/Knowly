from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent  # the backend/ folder


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIR / '.env')

    anthropic_api_key: str
    database_url: str
    model: str = 'claude-sonnet-5-5'


settings = Settings()