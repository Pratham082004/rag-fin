from fastapi import FastAPI
from sqlalchemy import text

from .config import settings
from app.database.database import engine


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)

@app.get("/")
def root():
    return {
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "Running"
    }

@app.get("/db")
def home():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))

    return {
        "message": "Database Connected Successfully"
    }