from app.config import settings
from app.services.vector_store.chroma import ChromaService


def get_vector_store():
    if settings.VECTOR_DB == "chroma":
        return ChromaService()

    raise ValueError("Unsupported vector database")