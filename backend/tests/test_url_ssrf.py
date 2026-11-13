"""SSRF protection, URL risk scoring, and PDF export tests."""

from __future__ import annotations

import pytest

from tests.conftest import register_and_get_headers


@pytest.mark.parametrize(
    "dangerous_url",
    [
        "http://localhost:8000/admin",
        "http://127.0.0.1/secret",
        "http://10.0.0.5/internal",
        "http://192.168.1.1/router",
        "http://169.254.169.254/latest/meta-data/",
        "http://[::1]:8080/",
        "http://[::ffff:127.0.0.1]/admin",
        "http://0.0.0.0:8000/",
        "http://0177.0.0.1/",
        "http://0x7f.0.0.1/",
        "http://2130706433/",
        "http://127.1/",
        "file:///etc/passwd",
        "javascript:alert(1)",
        "http://printer.local/config",
    ],
)
def test_ssrf_blocks_internal_and_unsafe_urls(client, dangerous_url):
    headers = register_and_get_headers(client, f"ssrf_{hash(dangerous_url)}@shop.in")
    resp = client.post("/api/urls/scan", headers=headers, json={"url": dangerous_url})
    assert resp.status_code == 400
    assert "blocked" in resp.json()["detail"].lower()


def test_suspicious_phishing_url_scored_and_exported(client):
    headers = register_and_get_headers(client, "urlscan@shop.in")
    resp = client.post(
        "/api/urls/scan",
        headers=headers,
        json={"url": "http://sbi-kyc-verify.login-check.xyz/update?redirect=http://evil.top"},
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["risk_score"] >= 50
    assert data["risk_category"] in ("High Risk", "Critical Risk")
    assert any(i["code"] == "brand_impersonation" for i in data["indicators"])

    detail = client.get(f"/api/urls/{data['id']}", headers=headers)
    assert detail.status_code == 200
    assert detail.json()["id"] == data["id"]

    pdf = client.get(f"/api/urls/{data['id']}/report.pdf", headers=headers)
    assert pdf.status_code == 200
    assert pdf.content.startswith(b"%PDF")

