from abc import ABC, abstractmethod
from typing import Any


class VectorStore(ABC):

    @abstractmethod
    async def create_collection(self) -> None:
        ...

    @abstractmethod
    async def upsert(
        self,
        vectors: list[list[float]],
        payloads: list[dict[str, Any]],
    ) -> None:
        ...

    @abstractmethod
    async def search(
        self,
        vector: list[float],
        limit: int = 5,
        ticker: str | None = None,
    ):
        ...

    @abstractmethod
    async def delete(
        self,
        filters: dict[str, Any],
    ) -> None:
        ...

    @abstractmethod
    async def health_check(self) -> bool:
        ...