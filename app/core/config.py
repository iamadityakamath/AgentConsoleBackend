from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
from functools import lru_cache


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    Uses pydantic-settings for validation and type coercion.
    """
    
    # Application
    APP_NAME: str = "Vedara Agent Console API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    
    # Server
    BASE_URL: str = "http://localhost:8000"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Security
    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database (optional)
    DATABASE_URL: str = ""
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"

    # LLM providers
    GROQ_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    API_KEY: str = ""
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["*"]
    ALLOWED_CREDENTIALS: bool = True
    ALLOWED_METHODS: List[str] = ["*"]
    ALLOWED_HEADERS: List[str] = ["*"]
    
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

    @property
    def groq_api_key(self) -> str:
        """Return the configured Groq API key."""

        return self.GROQ_API_KEY or self.API_KEY

    @property
    def openai_api_key(self) -> str:
        """Return the configured OpenAI API key."""

        return self.OPENAI_API_KEY or self.API_KEY or self.GROQ_API_KEY


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    
    Returns:
        Settings: Application settings
    """
    return Settings()
