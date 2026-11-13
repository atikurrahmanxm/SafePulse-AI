"""Application configuration loaded from environment variables with safe local defaults."""

from __future__ import annotations

import os
import secrets
from dataclasses import dataclass, field
from pathlib import Path
from typing import List


BASE_DIR = Path(__file__).resolve().parent.parent
ARTIFACT_DIR = BASE_DIR / "artifacts"
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)


def _split_csv(value: str) -> List[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "SafePulse AI")
    environment: str = os.getenv("ENVIRONMENT", "development")
    database_url: str = os.getenv("DATABASE_URL", f"sqlite:///{(BASE_DIR / 'safepulse.db').as_posix()}")
    jwt_secret_key: str = os.getenv(
        "JWT_SECRET_KEY",
        # Deterministic dev fallback only when not in production; override via env in prod.
        "safepulse-dev-secret-override-in-production-" + secrets.token_hex(8)
        if os.getenv("ENVIRONMENT") == "production"
        else "safepulse-ai-local-dev-secret-key-2026-adtu",
    )
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    jwt_expire_minutes: int = int(os.getenv("JWT_EXPIRE_MINUTES", "720"))
    cors_origins: List[str] = field(
        default_factory=lambda: _split_csv(
            os.getenv(
                "CORS_ORIGINS",
                "http://localhost:5173,http://127.0.0.1:5173,http://localhost:4173,http://127.0.0.1:4173",
            )
        )
    )
    rate_limit_per_minute: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "90"))
    google_safe_browsing_api_key: str = os.getenv("GOOGLE_SAFE_BROWSING_API_KEY", "").strip()
    virustotal_api_key: str = os.getenv("VIRUSTOTAL_API_KEY", "").strip()
    model_artifact_path: Path = ARTIFACT_DIR / "phishing_model.joblib"
    model_metrics_path: Path = ARTIFACT_DIR / "phishing_metrics.json"


settings = Settings()

