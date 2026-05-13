from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
import json

class Settings(BaseSettings):
    DATABASE_URL: str
    GEMINI_API_KEY: str
    SECRET_KEY: str
    CORS_ORIGINS: str
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    
    @property
    def get_cors_origins(self) -> List[str]:
        # Handle comma separated origins or single origin
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

settings = Settings()
