import json
from typing import Any, Dict, Optional
from pydantic import field_validator
from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    """Application settings loaded from .env file."""
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    # This replaces the load dotenv()

    # Environment
    ENVIRONMENT: str = "development"

    # Application
    # APP_TITLE: str = "Hashtag AI - Compliance Service"
    # APP_VERSION: str = "1.0.0"
    # API_HOST: str = "0.0.0.0"
    # API_PORT: int = 8007
    # MongoDB Configuration
    # MONGODB_URL: str = "mongodb://localhost:27017"
    # MONGODB_DB_NAME: str = "hashtag_ai_db"

    # GCP Configuration (Service Account JSON as string)
    GCP_SERVICE_ACCOUNT_JSON: str
    GCP_REGION: str = "asia-south1"

    @field_validator("GCP_SERVICE_ACCOUNT_JSON", mode="before")
    @classmethod
    def validate_gcp_json(cls, v: str) -> str:
        """Validate that GCP_SERVICE_ACCOUNT_JSON is valid JSON."""
        if v:
            try:
                json.loads(v)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON in GCP_SERVICE_ACCOUNT_JSON: {e}")
        return v

    @property
    def gcp_credentials(self) -> Dict[str, Any]:
        """Parse and return GCP credentials as dict."""
        return json.loads(self.GCP_SERVICE_ACCOUNT_JSON)

    @property
    def GCP_PROJECT_ID(self) -> str:
        """Extract project_id from service account JSON."""
        return self.gcp_credentials.get("project_id", "")

    # Gemini AI Configuration
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-2.0-flash"

    # Embeddings Configuration
    EMBEDDING_MODEL: str = "text-embedding-004"

    # ChromaDB Configuration
    CHROMA_PERSIST_DIR: str = "./data/chroma_db"

    # Mem0 Configuration
    MEM0_COLLECTION_NAME: str = "compliance_memories"
    MEM0_PERSIST_DIR: str = "./data/mem0_db"

    # RAG Configuration
    RAG_TOP_K: int = 5

    # Logging
    LOGS_DIR: str = "./logs"
    LOG_RETENTION_DAYS: int = 7

    # JWT Configuration (for future auth)
    JWT_SECRET_KEY: Optional[str] = None
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24

    # Observability Configuration
    TRACING_ENABLED: bool = False
    TRACE_RETENTION_DAYS: int = 7

    # Rate Limiting Configuration
    RATE_LIMITING_ENABLED: bool = False
    REDIS_URL: str = "redis://localhost:6379/0"

    @property
    def EXCEPTION_CONFIG(self) -> dict:
        """Get exception config based on environment."""
        if self.is_development:
            return DEV_EXCEPTION_CONFIG
        return PROD_EXCEPTION_CONFIG

    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.ENVIRONMENT.lower() in ["development", "dev", "local"]


# Singleton
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get cached settings instance."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
