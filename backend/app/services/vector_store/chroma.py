from __future__ import annotations

import logging
from typing import Any
from uuid import uuid4

import chromadb
from chromadb.config import Settings

from app.config import settings
from app.services.vector_store.base import VectorStore

logger = logging.getLogger(__name__)


class ChromaService(VectorStore):
    def __init__(self) -> None:

        self.client = chromadb.PersistentClient(
            path=settings.CHROMA_PATH,
            settings=Settings(anonymized_telemetry=False),
        )

        self.collection_name = settings.CHROMA_COLLECTION
        self.collection = None

    async def create_collection(self) -> None:

        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={
                "hnsw:space": "cosine",
            },
        )

        logger.info(
            "Chroma collection '%s' is ready.",
            self.collection_name,
        )

    def _ensure_collection(self):

        if self.collection is None:
            self.collection = self.client.get_collection(
                self.collection_name
            )

    async def upsert(
        self,
        vectors: list[list[float]],
        payloads: list[dict[str, Any]],
    ) -> None:

        self._ensure_collection()

        if len(vectors) != len(payloads):
            raise ValueError(
                "Vectors and payloads must have the same length."
            )

        ids = []
        embeddings = []
        metadatas = []
        documents = []

        for vector, payload in zip(vectors, payloads):

            ids.append(str(uuid4()))
            embeddings.append(vector)

            document = payload.pop("text", "")
            documents.append(document)

            metadatas.append(payload)

        self.collection.upsert(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
        )

        logger.info("Inserted %d vectors.", len(ids))

    async def search(
        self,
        vector: list[float],
        limit: int = 5,
        ticker: str | None = None,
    ):

        self._ensure_collection()

        where = None

        if ticker:
            where = {
                "ticker": ticker,
            }

        results = self.collection.query(
            query_embeddings=[vector],
            n_results=limit,
            where=where,
            include=[
                "documents",
                "metadatas",
                "distances",
            ],
        )

        return results

    async def delete(
        self,
        filters: dict[str, Any],
    ) -> None:

        self._ensure_collection()

        self.collection.delete(
            where=filters,
        )

        logger.info(
            "Deleted vectors matching %s",
            filters,
        )

    async def health_check(self) -> bool:

        try:
            self.client.heartbeat()
            return True

        except Exception as exc:
            logger.exception(exc)
            return False

    async def collection_exists(self) -> bool:

        collections = self.client.list_collections()

        names = [
            collection.name
            for collection in collections
        ]

        return self.collection_name in names

    async def close(self) -> None:
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(
        self,
        exc_type,
        exc_val,
        exc_tb,
    ):
        await self.close()