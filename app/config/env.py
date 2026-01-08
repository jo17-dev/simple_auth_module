from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore", 
        env_file= Path(__file__).parent.parent.parent / ".env", 
        env_file_encoding="utf-8"
    )
    DATABASE_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    PROJECT_NAME: str = "Simple auth mobule"
    API_VERSION: str
    ALGORITHM: str

settings = Settings()