from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # ==========================================================
    # Application
    # ==========================================================
    APP_NAME: str
    APP_VERSION: str
    DEBUG: bool

    # ==========================================================
    # Server
    # ==========================================================
    HOST: str
    PORT: int

    # ==========================================================
    # PostgreSQL
    # ==========================================================
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    # ==========================================================
    # Redis
    # ==========================================================
    REDIS_HOST: str
    REDIS_PORT: int

    # ==========================================================
    # Storage
    # ==========================================================
    REPORT_STORAGE: str

    # ==========================================================
    # Gemini
    # ==========================================================
    EMBEDDING_PROVIDER: str = "gemini"
    GEMINI_API_KEY: str
    GEMINI_EMBEDDING_MODEL: str = "gemini-embedding-001"

    # ==========================================================
    # Vector Store (ChromaDB)
    # ==========================================================
    VECTOR_DB: str = "chroma"
    CHROMA_PATH: str = "./storage/chroma"
    CHROMA_COLLECTION: str = "financial_rag"
    VECTOR_SIZE: int = 3072

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+psycopg2://"
            f"{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()