import logging

from app.retrieval.models import (
    RetrievalResult,
    SearchResult,
)

logger = logging.getLogger(__name__)


class RetrievalService:

    def __init__(
        self,
        embedding_service,
        vector_store,
    ):
        self.embedding_service = embedding_service
        self.vector_store = vector_store

    async def search(
        self,
        question: str,
        ticker: str | None = None,
        limit: int = 5,
    ) -> RetrievalResult:
        """
        Search the vector database for the most relevant chunks.

        Parameters
        ----------
        question : str
            User question.

        ticker : str | None
            Optional company ticker filter.

        limit : int
            Number of chunks to retrieve.

        Returns
        -------
        RetrievalResult
        """

        logger.info(
            "Searching documents for: %s",
            question,
        )

        # --------------------------------------------------
        # Embed the question
        # --------------------------------------------------

        query_vector = await self.embedding_service.embed(
            question
        )

        # --------------------------------------------------
        # Search ChromaDB
        # --------------------------------------------------

        raw_results = await self.vector_store.search(
            vector=query_vector,
            ticker=ticker,
            limit=limit,
        )

        documents = raw_results.get("documents", [[]])[0]
        metadatas = raw_results.get("metadatas", [[]])[0]
        distances = raw_results.get("distances", [[]])[0]

        results = []

        for document, metadata, distance in zip(
            documents,
            metadatas,
            distances,
        ):

            results.append(
                SearchResult(
                    text=document,
                    metadata=metadata,
                    score=1 - distance,
                )
            )

        logger.info(
            "Retrieved %d chunks",
            len(results),
        )

        return RetrievalResult(
            question=question,
            results=results,
        )