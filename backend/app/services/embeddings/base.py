from abc import ABC, abstractmethod
from typing import List


class EmbeddingProvider(ABC):
    """
    Base class for all embedding providers.
    """

    @abstractmethod
    async def embed(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.
        """
        raise NotImplementedError

    @abstractmethod
    async def embed_batch(
        self,
        texts: List[str]
    ) -> List[List[float]]:
        """
        Generate embeddings for multiple texts.
        """
        raise NotImplementedError