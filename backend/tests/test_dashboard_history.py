"""Dashboard aggregation, demo mode, and unified scan history tests."""

from __future__ import annotations

from tests.conftest import register_and_get_headers


def test_fresh_account_dashboard_empty_state_then_updates_from_db(client):
    headers = register_and_get_headers(client, "dash@shop.in", "Guwahati Mart")

    empty_dash = client.get("/api/dashboard/overview", headers=headers).json()
    assert empty_dash["is_empty"] is True
    assert empty_dash["summary"]["total_threat_analyses"] == 0
    assert empty_dash["summary"]["business_security_score"] is None

    # Run a real phishing analysis & URL scan
    client.post(
        "/api/phishing/analyze",
        headers=headers,
        json={
            "message": "URGENT: Your bank account is blocked. Enter OTP at http://sbi-kyc.xyz/login",
            "channel": "sms",
        },
    )
    client.post("/api/urls/scan", headers=headers, json={"url": "https://gst.gov.in/"})

    updated_dash = client.get("/api/dashboard/overview", headers=headers).json()
    assert updated_dash["is_empty"] is False
    assert updated_dash["summary"]["total_threat_analyses"] == 2
    assert updated_dash["summary"]["high_risk_findings"] >= 1

    history = client.get("/api/history/unified", headers=headers).json()
    assert len(history["items"]) == 2


def test_demo_mode_provides_labeled_sample_workspace(client):
    demo = client.post("/api/auth/demo")
    assert demo.status_code == 200
    payload = demo.json()
    assert payload["user"]["is_demo"] is True
    assert payload["user"]["business"]["is_demo_workspace"] is True

    headers = {"Authorization": f"Bearer {payload['access_token']}"}
    dash = client.get("/api/dashboard/overview", headers=headers).json()
    assert dash["is_empty"] is False
    assert dash["summary"]["total_threat_analyses"] >= 4
    assert all(p["is_demo_sample"] is True for p in dash["recent_phishing"])

