"""Incident Response Center and Employee Cyber Awareness tests."""

from __future__ import annotations

from tests.conftest import register_and_get_headers


def test_incident_lifecycle_and_checklist_progress(client):
    headers = register_and_get_headers(client, "inc@shop.in")
    scenarios = client.get("/api/incidents/scenarios", headers=headers)
    assert scenarios.status_code == 200
    assert len(scenarios.json()["scenarios"]) == 7

    created = client.post(
        "/api/incidents",
        headers=headers,
        json={"scenario_key": "phishing_link_clicked", "notes": "Clicked on counter PC"},
    )
    assert created.status_code == 201
    inc = created.json()
    assert inc["total_count"] == 6
    assert inc["progress_percent"] == 0
    assert inc["status"] == "in_progress"

    # Complete all checklist items -> incident auto-transitions to resolved
    for item in inc["checklist_items"]:
        upd = client.patch(
            f"/api/incidents/{inc['id']}/items/{item['id']}",
            headers=headers,
            json={"is_completed": True},
        )
        assert upd.status_code == 200
        inc = upd.json()

    assert inc["progress_percent"] == 100
    assert inc["status"] == "resolved"

    pdf = client.get(f"/api/incidents/{inc['id']}/report.pdf", headers=headers)
    assert pdf.status_code == 200
    assert pdf.content.startswith(b"%PDF")


def test_awareness_quiz_submission_and_progress(client):
    headers = register_and_get_headers(client, "aware@shop.in")
    overview = client.get("/api/awareness/overview", headers=headers)
    assert overview.status_code == 200
    data = overview.json()
    assert len(data["lessons"]) >= 4
    assert all(sim["is_training_simulation"] for sim in data["simulations"])

    submit = client.post(
        "/api/awareness/quizzes/phishing-defense-essentials/submit",
        headers=headers,
        json={"answers": {"q1": 0, "q2": 1, "q3": 1, "q4": 1}},
    )
    assert submit.status_code == 201
    assert submit.json()["score"] == 4
    assert submit.json()["percentage"] == 100.0

    overview_after = client.get("/api/awareness/overview", headers=headers).json()
    assert overview_after["progress"]["completed_quizzes"] == 1
    assert overview_after["progress"]["average_score"] == 100.0

