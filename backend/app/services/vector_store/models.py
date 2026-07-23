from dataclasses import dataclass
from typing import Any


@dataclass
class SearchResult:

    id: str

    score: float

    payload: dict[str, Any]