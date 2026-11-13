"""Tests for multi-business workspaces, governance controls, MFA team tracking, integrations, incident workflow, and monthly reports."""

from __future__ import annotations

from tests.conftest import register_and_get_headers


def test_multi_business_workspace_isolation_and_switching(client):
    headers_a = register_and_get_headers(client, "multi_a@shop.in", "Shop Alpha")
    headers_b = register_and_get_headers(client, "multi_b@shop.in", "Shop Beta")

    # Owner A creates a second business workspace
    create_resp = client.post(
        "/api/auth/businesses",
        headers=headers_a,
        json={"name": "Shop Alpha Branch 2", "industry": "Pharmacy", "employee_count": 4, "city": "Jorhat"},
    )
    assert create_resp.status_code == 201
    branch_id = create_resp.json()["id"]

    me_a = client.get("/api/auth/me", headers=headers_a)
    assert me_a.status_code == 200
    assert len(me_a.json()["businesses"]) == 2

    # Owner A switches context to branch_id via X-Business-Id and submits a phishing scan
    scoped_headers_a = {**headers_a, "X-Business-Id": str(branch_id)}
    scan_resp = client.post(
        "/api/phishing/analyze",
        headers=scoped_headers_a,
        json={"message": "URGENT: Your SBI KYC is blocked. Enter OTP at http://sbi-kyc.xyz/login", "channel": "sms"},
    )
    assert scan_resp.status_code == 201
    assert len(scan_resp.json()["social_engineering_tactics"]) >= 1

    # Primary workspace still has 0 scans (clean multi-workspace isolation)
    ov_primary = client.get("/api/dashboard/overview", headers=headers_a).json()
    ov_branch = client.get("/api/dashboard/overview", headers=scoped_headers_a).json()
    assert ov_primary["summary"]["total_threat_analyses"] == 0
    assert ov_branch["summary"]["total_threat_analyses"] == 1

    # Owner B attempting to use Owner A's workspace header MUST receive 403 Forbidden
    intrusion = client.get("/api/dashboard/overview", headers={**headers_b, "X-Business-Id": str(branch_id)})
    assert intrusion.status_code == 403


def test_governance_members_controls_integrations_and_monthly_pdf(client):
    headers = register_and_get_headers(client, "gov@shop.in", "Kamrup Traders")

    # Initial governance overview seeds 12 default operational controls
    gov = client.get("/api/governance/overview", headers=headers)
    assert gov.status_code == 200
    assert gov.headers.get("X-API-Version") == "1.0.0"
    assert gov.headers.get("X-Frame-Options") == "DENY"
    gov_data = gov.json()
    assert gov_data["controls_stats"]["total_count"] >= 10
    assert gov_data["mfa_stats"]["mfa_adoption_percent"] == 0

    # Add 2 team members (1 MFA ON, 1 MFA OFF -> 50% MFA adoption)
    m1 = client.post(
        "/api/governance/members",
        headers=headers,
        json={"full_name": "Neha Bora", "email": "neha@kamrup.in", "role": "manager", "department": "Accounts", "mfa_enabled": True, "awareness_trained": True},
    )
    m2 = client.post(
        "/api/governance/members",
        headers=headers,
        json={"full_name": "Amit Roy", "email": "amit@kamrup.in", "role": "staff", "department": "Counter", "mfa_enabled": False, "awareness_trained": False},
    )
    assert m1.status_code == 201 and m2.status_code == 201

    # Toggle first operational control completed
    first_ctrl_id = gov_data["controls"][0]["id"]
    ctrl_upd = client.patch(
        f"/api/governance/controls/{first_ctrl_id}",
        headers=headers,
        json={"is_completed": True, "owner_name": "Neha Bora"},
    )
    assert ctrl_upd.status_code == 200
    assert ctrl_upd.json()["is_completed"] is True

    # Configure future integration readiness metadata
    int_resp = client.put(
        "/api/governance/integrations/google_workspace",
        headers=headers,
        json={"enabled": True, "endpoint_or_account": "kamrup.in", "notes": "Pending Admin SDK OAuth"},
    )
    assert int_resp.status_code == 200

    # Verify dashboard reflects 50% MFA adoption and filtered date query
    ov = client.get("/api/dashboard/overview?days=30", headers=headers)
    assert ov.status_code == 200
    prog = ov.json()["improvement_progress"]
    assert prog["mfa_adoption_percent"] == 50
    assert prog["controls_completed"] == 1

    # Export Monthly Business Security Report PDF
    pdf = client.get("/api/reports/monthly.pdf", headers=headers)
    assert pdf.status_code == 200
    assert pdf.content.startswith(b"%PDF")


def test_incident_workflow_assignee_timeline_and_url_verdict(client):
    headers = register_and_get_headers(client, "inc_adv@shop.in", "Barak Stores")

    # Create incident and update assignee, status, resolution, and timeline notes
    create = client.post(
        "/api/incidents",
        headers=headers,
        json={"scenario_key": "phishing_link_clicked", "assigned_to": "Suman Das", "notes": "Customer QR mismatch"},
    )
    assert create.status_code == 201
    inc = create.json()
    inc_id = inc["id"]
    assert inc["assigned_to"] == "Suman Das"
    assert len(inc["timeline_notes"]) == 1

    upd = client.patch(
        f"/api/incidents/{inc_id}",
        headers=headers,
        json={"status": "contained", "severity": "Critical", "resolution_summary": "Reported to 1930; bank account frozen temporarily."},
    )
    assert upd.status_code == 200
    assert upd.json()["status"] == "contained"
    assert upd.json()["severity"] == "Critical"

    note = client.post(
        f"/api/incidents/{inc_id}/notes",
        headers=headers,
        json={"content": "Submitted ACK #1930-99210 on cybercrime.gov.in"},
    )
    assert note.status_code == 201
    assert len(note.json()["timeline_notes"]) >= 3

    pdf = client.get(f"/api/incidents/{inc_id}/report.pdf", headers=headers)
    assert pdf.status_code == 200 and pdf.content.startswith(b"%PDF")

    # URL scan includes verdict_classification and tls_info
    url_scan = client.post(
        "/api/urls/scan",
        headers=headers,
        json={"url": "http://sbi-kyc-update.xyz/login"},
    )
    assert url_scan.status_code == 201
    u_data = url_scan.json()
    assert u_data["verdict_classification"] in ("Suspicious", "Malicious")
    assert isinstance(u_data["tls_info"], dict)
