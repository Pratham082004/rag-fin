from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class settings(BaseSettings):
    # configuration for App
    APP_NAME: str
    APP_VERSION: str
    DEBUG: bool

    # configuration for Server
    HOST: str
    PORT: int

    # configuration for Database
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    # configuration for OpenAI
    OPENAI_API_KEY: str

    # configuration for Qdrant
    QDRANT_HOST: str
    QDRANT_PORT: int

    # configuration for Redis
    REDIS_HOST: str
    REDIS_PORT: int

    # configuration for Storage
    REPORT_STORAGE: str

    # configuration for AI  
    EMBEDDING_PROVIDER: str = "gemini"
    GEMINI_API_KEY: str
    GEMINI_EMBEDDING_MODEL: str = "gemini-embedding-001"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+psycopg2://"
            f"{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


@lru_cache
def get_settings() -> settings:
    return settings()


settings = get_settings()