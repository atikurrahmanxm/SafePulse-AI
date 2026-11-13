"""SQLAlchemy database configuration supporting SQLite (dev) and PostgreSQL (prod)."""

from __future__ import annotations

from sqlalchemy import create_engine, event, inspect, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from .config import settings


def _build_engine():
    url = settings.database_url
    connect_args = {}
    if url.startswith("sqlite"):
        connect_args = {"check_same_thread": False}
    engine = create_engine(url, connect_args=connect_args, pool_pre_ping=True)

    if url.startswith("sqlite"):
        @event.listens_for(engine, "connect")
        def _set_sqlite_pragma(dbapi_connection, _connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

    return engine


engine = _build_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Base declarative class for all ORM entities."""


def get_db():
    """FastAPI dependency yielding a scoped SQLAlchemy session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def ensure_schema_extensions(target_engine=None) -> None:
    """Safely add additive columns to pre-existing SQLite/PostgreSQL tables during upgrades."""
    eng = target_engine or engine
    inspector = inspect(eng)
    existing_tables = set(inspector.get_table_names())

    additive_columns = {
        "businesses": [
            ("subscription_tier", "VARCHAR(32) NOT NULL DEFAULT 'free'"),
            ("monthly_scan_quota", "INTEGER NOT NULL DEFAULT 50"),
        ],
        "phishing_analyses": [
            ("social_engineering_tactics", "JSON NOT NULL DEFAULT '[]'"),
        ],
        "url_scans": [
            ("verdict_classification", "VARCHAR(48) NOT NULL DEFAULT 'Unknown'"),
            ("tls_info", "JSON NOT NULL DEFAULT '{}'"),
        ],
        "incidents": [
            ("assigned_to", "VARCHAR(120)"),
            ("resolution_summary", "TEXT"),
        ],
    }

    with eng.begin() as conn:
        for table_name, cols in additive_columns.items():
            if table_name not in existing_tables:
                continue
            current_cols = {c["name"] for c in inspector.get_columns(table_name)}
            for col_name, col_ddl in cols:
                if col_name not in current_cols:
                    conn.execute(text(f"ALTER TABLE {table_name} ADD COLUMN {col_name} {col_ddl}"))

