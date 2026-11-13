"""Pytest fixtures with an isolated temporary SQLite test database."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app
from app.security import rate_limiter


@pytest.fixture(scope="function")
def client(tmp_path):
    db_file = tmp_path / "test_safepulse.db"
    engine = create_engine(f"sqlite:///{db_file.as_posix()}", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    rate_limiter.reset()

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    engine.dispose()


def register_and_get_headers(client: TestClient, email: str, business_name: str = "Test Shop"):
    resp = client.post(
        "/api/auth/register",
        json={
            "email": email,
            "password": "StrongPassword123",
            "full_name": "Test Owner",
            "business_name": business_name,
            "industry": "Retail",
            "employee_count": 6,
            "city": "Guwahati",
        },
    )
    assert resp.status_code == 201, resp.text
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

