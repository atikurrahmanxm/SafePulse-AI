"""Authentication, password hashing, tenant isolation, input validation, and rate limit tests."""

from __future__ import annotations

from app.security import hash_password, verify_password
from tests.conftest import register_and_get_headers


def test_argon2_password_hashing():
    hashed = hash_password("SafePulse2026!")
    assert hashed.startswith("$argon2")
    assert verify_password("SafePulse2026!", hashed)
    assert not verify_password("WrongPassword1", hashed)


def test_register_login_and_me(client):
    headers = register_and_get_headers(client, "alice@pharmacy.in", "Alice Pharmacy")
    me = client.get("/api/auth/me", headers=headers)
    assert me.status_code == 200
    data = me.json()
    assert data["email"] == "alice@pharmacy.in"
    assert data["business"]["name"] == "Alice Pharmacy"

    login_ok = client.post(
        "/api/auth/login",
        json={"email": "alice@pharmacy.in", "password": "StrongPassword123"},
    )
    assert login_ok.status_code == 200
    assert "access_token" in login_ok.json()

    login_bad = client.post(
        "/api/auth/login",
        json={"email": "alice@pharmacy.in", "password": "IncorrectPassword1"},
    )
    assert login_bad.status_code == 401


def test_unauthenticated_endpoints_rejected(client):
    assert client.get("/api/dashboard/overview").status_code == 401
    assert client.post("/api/phishing/analyze", json={"message": "Verify account urgently"}).status_code == 401
    assert client.post("/api/urls/scan", json={"url": "https://example.com"}).status_code == 401


def test_business_data_isolation(client):
    headers_a = register_and_get_headers(client, "owner_a@shop.in", "Shop A")
    headers_b = register_and_get_headers(client, "owner_b@shop.in", "Shop B")

    scan_a = client.post(
        "/api/phishing/analyze",
        headers=headers_a,
        json={
            "message": "URGENT: Your SBI corporate bank account is suspended. Verify OTP at http://sbi-kyc.xyz/login",
            "channel": "sms",
        },
    )
    assert scan_a.status_code == 201
    analysis_id = scan_a.json()["id"]

    # Owner B must not see Owner A's phishing history or PDF report
    hist_b = client.get("/api/phishing/history", headers=headers_b)
    assert hist_b.status_code == 200
    assert len(hist_b.json()) == 0

    pdf_b = client.get(f"/api/phishing/{analysis_id}/report.pdf", headers=headers_b)
    assert pdf_b.status_code == 404

    detail_b = client.get(f"/api/phishing/{analysis_id}", headers=headers_b)
    assert detail_b.status_code == 404


def test_rate_limiting_enforced_on_login(client):
    for _ in range(30):
        client.post("/api/auth/login", json={"email": "nobody@shop.in", "password": "x"})
    blocked = client.post("/api/auth/login", json={"email": "nobody@shop.in", "password": "x"})
    assert blocked.status_code == 429

