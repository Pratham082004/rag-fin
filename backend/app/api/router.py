from fastapi import APIRouter

from app.api.chats import router as chat_router
from app.api.ingest import router as ingest_router
from app.api.health import router as health_router

api_router = APIRouter()

api_router.include_router(
    health_router,
    prefix="/health",
    tags=["Health"],
)

api_router.include_router(
    ingest_router,
    prefix="/ingest",
    tags=["Ingestion"],
)

api_router.include_router(
    chat_router,
    prefix="/chat",
    tags=["Chat"],
)