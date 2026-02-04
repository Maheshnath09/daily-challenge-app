"""
Application configuration settings.
Uses pydantic-settings for environment variable management.
"""
import json
from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List, Union


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # App settings
    APP_NAME: str = "Daily Challenge App"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/dailychallenge"
    
    # JWT Settings
    SECRET_KEY: str = "your-super-secret-key-change-in-production-minimum-32-characters"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # CORS - stored as string, parsed by property
    CORS_ORIGINS: str = '["http://localhost:3000", "http://127.0.0.1:3000"]'
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS_ORIGINS to a list."""
        v = self.CORS_ORIGINS
        if not v:
            return ["*"]
        # Handle wildcard
        if v.strip() == "*":
            return ["*"]
        # Try JSON parsing first
        try:
            parsed = json.loads(v)
            if isinstance(parsed, list):
                return parsed
        except json.JSONDecodeError:
            pass
        # Fall back to comma-separated
        return [origin.strip() for origin in v.split(',') if origin.strip()]
    
    @field_validator('DATABASE_URL', mode='before')
    @classmethod
    def fix_database_url(cls, v: str) -> str:
        """Fix postgres:// scheme for SQLAlchemy compatibility."""
        if v and v.startswith("postgres://"):
            return v.replace("postgres://", "postgresql+asyncpg://", 1)
        return v
    
    class Config:
        env_file = ".env"
        extra = "allow"


def get_settings() -> Settings:
    """Get settings instance."""
    return Settings()


settings = get_settings()


