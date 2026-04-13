from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
from functools import lru_cache
import json


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
    ALLOWED_ORIGINS: str = "[\"*\"]"
    ALLOWED_CREDENTIALS: str = "true"
    ALLOWED_METHODS: str = "[\"*\"]"
    ALLOWED_HEADERS: str = "[\"*\"]"
    
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

    @staticmethod
    def _parse_list_env(value: object) -> List[str] | object:
        """Parse list-like env values from JSON array, CSV string, or wildcard."""

        if isinstance(value, list):
            return [str(v).strip() for v in value if str(v).strip()]

        if not isinstance(value, str):
            return value

        raw = value.strip()
        if not raw:
            return []

        if raw == "*":
            return ["*"]

        if raw.startswith("[") and raw.endswith("]"):
            try:
                parsed = json.loads(raw)
                if isinstance(parsed, list):
                    return [str(v).strip() for v in parsed if str(v).strip()]
            except Exception:
                pass

        return [part.strip() for part in raw.split(",") if part.strip()]

    @property
    def allowed_origins(self) -> List[str]:
        """Return CORS origins as list from JSON array, CSV, or wildcard string."""

        parsed = self._parse_list_env(self.ALLOWED_ORIGINS)
        return parsed if isinstance(parsed, list) else ["*"]

    @property
    def allowed_methods(self) -> List[str]:
        """Return CORS methods as list from JSON array, CSV, or wildcard string."""

        parsed = self._parse_list_env(self.ALLOWED_METHODS)
        return parsed if isinstance(parsed, list) else ["*"]

    @property
    def allowed_headers(self) -> List[str]:
        """Return CORS headers as list from JSON array, CSV, or wildcard string."""

        parsed = self._parse_list_env(self.ALLOWED_HEADERS)
        return parsed if isinstance(parsed, list) else ["*"]

    @property
    def allowed_credentials(self) -> bool:
        """Return CORS credentials flag parsed from string/bool env value."""

        raw = self.ALLOWED_CREDENTIALS
        if isinstance(raw, bool):
            return raw
        lowered = str(raw).strip().lower()
        return lowered in {"1", "true", "yes", "y", "on"}

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
