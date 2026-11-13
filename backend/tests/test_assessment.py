"""Business Security Health Check scoring, categories, and PDF export tests."""

from __future__ import annotations

from tests.conftest import register_and_get_headers


def test_assessment_scoring_bands_and_pdf(client):
    headers = register_and_get_headers(client, "assess@shop.in")
    q_resp = client.get("/api/assessments/questions", headers=headers)
    assert q_resp.status_code == 200
    questions = q_resp.json()["questions"]
    assert len(questions) == 10

    # All "no" -> 0 Critical
    low_answers = {q["key"]: "no" for q in questions}
    res_low = client.post("/api/assessments/submit", headers=headers, json={"answers": low_answers})
    assert res_low.status_code == 201
    assert res_low.json()["overall_score"] == 0
    assert res_low.json()["security_category"] == "Critical"
    assert len(res_low.json()["critical_gaps"]) == 10

    # All "yes" -> 100 Strong
    high_answers = {q["key"]: "yes" for q in questions}
    res_high = client.post("/api/assessments/submit", headers=headers, json={"answers": high_answers})
    assert res_high.status_code == 201
    assert res_high.json()["overall_score"] == 100
    assert res_high.json()["security_category"] == "Strong"
    assert len(res_high.json()["critical_gaps"]) == 0

    pdf = client.get(f"/api/assessments/{res_low.json()['id']}/report.pdf", headers=headers)
    assert pdf.status_code == 200
    assert pdf.content.startswith(b"%PDF")

