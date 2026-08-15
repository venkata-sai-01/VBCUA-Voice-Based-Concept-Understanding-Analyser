from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "VBCUA"
    database_url: str = "sqlite:///data/vbcua.db"
    whisper_model: str = "base"
    embedding_model: str = "all-MiniLM-L6-v2"
    max_audio_seconds: int = 600
    report_dir: str = "reports"
    cors_origins: str = "*"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

@lru_cache
def get_settings():
    return Settings()
