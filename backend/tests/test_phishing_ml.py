"""ML phishing detection pipeline, held-out evaluation, phrase highlighting, and PDF export tests."""

from __future__ import annotations

from tests.conftest import register_and_get_headers


def test_ml_evaluation_endpoint_reports_real_metrics(client):
    headers = register_and_get_headers(client, "ml@shop.in")
    resp = client.get("/api/phishing/model-evaluation", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    metrics = data["held_out_metrics"]
    assert 0.7 <= metrics["precision"] <= 1.0
    assert 0.7 <= metrics["recall"] <= 1.0
    assert 0.7 <= metrics["f1_score"] <= 1.0
    cm = metrics["confusion_matrix"]
    assert cm["tn"] + cm["fp"] + cm["fn"] + cm["tp"] == data["dataset"]["held_out_test_size"]
    assert len(data["limitations"]) >= 2


def test_phishing_high_risk_and_low_risk_classification(client):
    headers = register_and_get_headers(client, "phish@shop.in")

    scam_resp = client.post(
        "/api/phishing/analyze",
        headers=headers,
        json={
            "message": (
                "FINAL NOTICE: Your HDFC netbanking account is blocked tonight. "
                "Enter your OTP and ATM PIN immediately at http://hdfc-secure-unlock.top/verify"
            ),
            "channel": "sms",
            "sender_hint": "alert@gmail.com",
        },
    )
    assert scam_resp.status_code == 201
    scam = scam_resp.json()
    assert scam["risk_score"] >= 70
    assert scam["risk_category"] in ("High Risk", "Critical Risk")
    assert len(scam["highlighted_phrases"]) >= 1
    assert len(scam["reasons"]) >= 1
    assert len(scam["recommendations"]) >= 1

    legit_resp = client.post(
        "/api/phishing/analyze",
        headers=headers,
        json={
            "message": (
                "Hi Priya, attached is our monthly medicine supply invoice #INV-2026-0412 for Rs 32,450 "
                "as discussed on yesterday's call. Payment terms remain Net 15."
            ),
            "channel": "email",
        },
    )
    assert legit_resp.status_code == 201
    legit = legit_resp.json()
    assert legit["risk_score"] < 40
    assert legit["risk_category"] in ("Low Risk", "Moderate Risk")

    detail_resp = client.get(f"/api/phishing/{scam['id']}", headers=headers)
    assert detail_resp.status_code == 200
    assert detail_resp.json()["id"] == scam["id"]

    pdf_resp = client.get(f"/api/phishing/{scam['id']}/report.pdf", headers=headers)
    assert pdf_resp.status_code == 200
    assert pdf_resp.headers["content-type"] == "application/pdf"
    assert pdf_resp.content.startswith(b"%PDF")


def test_phishing_validation_rejects_short_message(client):
    headers = register_and_get_headers(client, "val@shop.in")
    bad = client.post("/api/phishing/analyze", headers=headers, json={"message": "short", "channel": "sms"})
    assert bad.status_code == 422

