from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class SearchResult:
    """
    A single retrieved chunk from the vector database.
    """

    text: str
    metadata: dict[str, Any]
    score: float


@dataclass(slots=True)
class RetrievalResult:
    """
    Collection of retrieved chunks.
    """

    question: str
    results: list[SearchResult]