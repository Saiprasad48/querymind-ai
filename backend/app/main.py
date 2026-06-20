from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routes.db import router as db_router
from app.routes.query import router as query_router
from app.routes.ai import router as ai_router
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(db_router)
app.include_router(query_router)
app.include_router(ai_router)

@app.get("/")
def root():
    return {
        "message": "Welcome to QueryMind AI",
        "status": "running"
    }
@app.get("/health")
def health_check():
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "healthy"
    }