from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.router import api_router
from app.dependencies import get_company_cache


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup and shutdown events.
    """

    # Startup
    cache = get_company_cache()

    try:
        await cache.load()
        print(
            f"✅ Loaded {len(cache.company_records)} SEC companies."
        )
    except Exception as exc:
        print(f"❌ Failed to load SEC company cache: {exc}")
        raise

    yield

    # Shutdown
    print("👋 Financial RAG API shutting down.")


app = FastAPI(
    title="Financial RAG API",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(api_router)


@app.get("/")
async def root():
    return {
        "message": "Financial RAG API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
    }