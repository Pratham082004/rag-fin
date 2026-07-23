import asyncio
import logging
from typing import List

from google import genai

from app.config import settings
from app.services.embeddings.base import EmbeddingProvider

logger = logging.getLogger(__name__)


class GeminiEmbeddingProvider(EmbeddingProvider):

    def __init__(self):

        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

        self.model = settings.GEMINI_EMBEDDING_MODEL

    async def embed(
        self,
        text: str,
    ) -> List[float]:

        retries = 3

        for attempt in range(retries):

            try:

                response = self.client.models.embed_content(
                    model=self.model,
                    contents=text,
                )

                return response.embeddings[0].values

            except Exception as e:

                logger.warning(
                    "Embedding failed (%s/%s): %s",
                    attempt + 1,
                    retries,
                    e,
                )

                if attempt == retries - 1:
                    raise

                await asyncio.sleep(2 ** attempt)

    async def embed_batch(
        self,
        texts: List[str],
    ) -> List[List[float]]:

        vectors = []

        for text in texts:

            vectors.append(
                await self.embed(text)
            )

        return vectors