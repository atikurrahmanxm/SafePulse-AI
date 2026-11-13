"""Tests for Data Breach & Credential Exposure Monitoring Engine and Endpoints."""

import pytest
from app.services.breach_engine import check_breach_exposure
from tests.conftest import register_and_get_headers


def test_breach_engine_detects_compromised_query():
    res = check_breach_exposure("owner@pharmacy.in", language="en")
    assert res["query"] == "owner@pharmacy.in"
    assert res["query_type"] == "email"
    assert res["exposure_count"] >= 1
    assert res["risk_score"] > 20
    assert len(res["breaches"]) >= 1
    assert len(res["recommended_actions"]) >= 3


def test_breach_engine_handles_clean_query():
    res = check_breach_exposure("clean-user@safe-example.com", language="en")
    assert res["query"] == "clean-user@safe-example.com"
    assert res["exposure_count"] == 0
    assert res["risk_level"] == "Low"
    assert res["risk_score"] <= 20
    assert len(res["breaches"]) == 0


def test_breach_endpoint_authenticated_check(client):
    headers = register_and_get_headers(client, "alice_breach@shop.in", "Alice Retail Store")
    resp = client.post(
        "/api/breaches/check",
        json={"query": "billing@retailpos-cloud.in", "language": "en"},
        headers=headers,
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["query"] == "billing@retailpos-cloud.in"
    assert data["exposure_count"] >= 1
    assert "Passwords" in data["data_classes_exposed"]


def test_breach_pdf_download(client):
    headers = register_and_get_headers(client, "bob_breach@shop.in", "Bob Pharmacy")
    resp = client.get(
        "/api/breaches/report.pdf?query=owner@pharmacy.in&language=en",
        headers=headers,
    )
    assert resp.status_code == 200
    assert resp.headers["content-type"] == "application/pdf"
    assert len(resp.content) > 500

