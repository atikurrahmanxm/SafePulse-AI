"""FastAPI application entry point for SafePulse AI."""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .database import Base, SessionLocal, engine, ensure_schema_extensions
from .ml.trainer import get_model_and_metrics
from .routers import (
    assessment,
    auth,
    awareness,
    dashboard,
    governance,
    history,
    incidents,
    phishing,
    url_scanner,
)
from .services.demo_seeder import ensure_quizzes_seeded


@asynccontextmanager
async def lifespan(_app: FastAPI):
    Base.metadata.create_all(bind=engine)
    ensure_schema_extensions(engine)
    get_model_and_metrics()
    db = SessionLocal()
    try:
        ensure_quizzes_seeded(db)
    finally:
        db.close()
    yield


app = FastAPI(
    title="SafePulse AI API",
    description="AI-Powered Small Business Cybersecurity Platform — AdtU Innovation Mela 2026",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-Business-Id"],
)


@app.middleware("http")
async def security_and_version_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-API-Version"] = "1.0.0"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    return response


app.include_router(auth.router)
app.include_router(dashboard.router)
app.include_router(phishing.router)
app.include_router(url_scanner.router)
app.include_router(assessment.router)
app.include_router(incidents.router)
app.include_router(awareness.router)
app.include_router(history.router)
app.include_router(governance.router)


@app.get("/api/health", tags=["System"])
def health_check():
    return {
        "status": "ok",
        "service": settings.app_name,
        "environment": settings.environment,
    }

