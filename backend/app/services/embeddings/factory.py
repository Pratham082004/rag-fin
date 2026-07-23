from app.config import settings
from app.services.embeddings.base import EmbeddingProvider
from app.services.embeddings.gemini import GeminiEmbeddingProvider


def get_embedding_provider() -> EmbeddingProvider:

    provider = settings.EMBEDDING_PROVIDER.lower()

    if provider == "gemini":
        return GeminiEmbeddingProvider()

    raise ValueError(
        f"Unsupported embedding provider: {provider}"
    )