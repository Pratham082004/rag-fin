from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_rag_service
from app.retrieval.rag_service import RAGService
from app.schemas.chats import (
    ChatRequest,
    ChatResponse,
)

router = APIRouter()


@router.post(
    "/",
    response_model=ChatResponse,
)
async def chat(
    request: ChatRequest,
    rag_service: RAGService = Depends(get_rag_service),
):

    try:

        result = await rag_service.ask(
            question=request.question,
            limit=request.limit,
        )

        return ChatResponse(
            answer=result["answer"],
            sources=result["sources"],
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )