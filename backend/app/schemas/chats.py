from pydantic import BaseModel


class Source(BaseModel):

    section: str | None
    score: float


class ChatRequest(BaseModel):

    question: str
    limit: int = 5


class ChatResponse(BaseModel):

    answer: str
    sources: list[Source]