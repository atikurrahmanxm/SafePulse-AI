"""Branded PDF report generator using ReportLab for Phishing, URL, Assessment, and Incident reports."""

from __future__ import annotations

from io import BytesIO
from typing import Any, Dict, List
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


NAVY = colors.HexColor("#080D1B")
INDIGO = colors.HexColor("#4F46E5")
CYAN = colors.HexColor("#0891B2")
SLATE = colors.HexColor("#334155")
MUTED = colors.HexColor("#64748B")
LIGHT_BG = colors.HexColor("#F1F5F9")
BORDER = colors.HexColor("#CBD5E1")


def _build_pdf(
    report_title: str,
    business_name: str,
    generated_at: str,
    summary_rows: List[List[str]],
    sections: List[Dict[str, Any]],
    limitation_note: str,
) -> bytes:
    buf = BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
        title=f"SafePulse AI - {report_title}",
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "CS_Title",
        parent=styles["Heading1"],
        fontSize=18,
        leading=22,
        textColor=NAVY,
        spaceAfter=4,
    )
    subtitle_style = ParagraphStyle(
        "CS_Sub",
        parent=styles["Normal"],
        fontSize=9.5,
        textColor=MUTED,
        spaceAfter=12,
    )
    h2_style = ParagraphStyle(
        "CS_H2",
        parent=styles["Heading2"],
        fontSize=12,
        leading=16,
        textColor=INDIGO,
        spaceBefore=10,
        spaceAfter=5,
    )
    body_style = ParagraphStyle(
        "CS_Body",
        parent=styles["Normal"],
        fontSize=9.5,
        leading=14,
        textColor=SLATE,
        spaceAfter=4,
    )
    note_style = ParagraphStyle(
        "CS_Note",
        parent=styles["Normal"],
        fontSize=8.5,
        leading=12,
        textColor=MUTED,
    )

    story: List[Any] = [
        Paragraph("SafePulse AI — Small Business Security Report", subtitle_style),
        Paragraph(escape(report_title), title_style),
        Paragraph(
            f"Business: <b>{escape(business_name)}</b> &nbsp;|&nbsp; Generated: {escape(generated_at)}",
            subtitle_style,
        ),
    ]

    if summary_rows:
        table = Table(summary_rows, colWidths=[48 * mm, 126 * mm])
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (0, -1), LIGHT_BG),
                    ("TEXTCOLOR", (0, 0), (0, -1), NAVY),
                    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, -1), 9),
                    ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("PADDING", (0, 0), (-1, -1), 6),
                ]
            )
        )
        story.append(table)
        story.append(Spacer(1, 10))

    for sec in sections:
        story.append(Paragraph(escape(sec["heading"]), h2_style))
        if sec.get("text"):
            story.append(Paragraph(escape(sec["text"]), body_style))
        for item in sec.get("items", []):
            story.append(Paragraph(f"&bull; {escape(str(item))}", body_style))

    story.append(Spacer(1, 12))
    story.append(Paragraph("Important Limitations & Responsible Notice", h2_style))
    story.append(Paragraph(escape(limitation_note), note_style))

    doc.build(story)
    return buf.getvalue()


def generate_phishing_pdf(record: Any, business_name: str) -> bytes:
    summary = [
        ["Risk Score", f"{record.risk_score} / 100 ({record.risk_category})"],
        ["Channel", record.channel.upper()],
        ["ML Probability", f"{record.ml_probability * 100:.1f}%"],
        ["Model Confidence", f"{record.model_confidence * 100:.0f}%"],
        ["Analyzed At", record.created_at.isoformat()],
    ]
    phrases = [
        f"\"{p.get('phrase', '')}\" ({p.get('category', 'indicator')})"
        for p in (record.highlighted_phrases or [])
    ]
    sections = [
        {"heading": "Analyzed Message Excerpt", "text": record.raw_message[:1200]},
        {"heading": "Evidence & Highlighted Phrases", "items": phrases or ["No specific suspicious phrase spans matched."]},
        {"heading": "Classification Reasons", "items": record.reasons or []},
        {"heading": "Recommended Security Actions", "items": record.recommendations or []},
    ]
    limitation = (
        "Risk scores (0-24 Low, 25-49 Moderate, 50-74 High, 75-100 Critical) are SafePulse AI application thresholds. "
        "Automated ML/heuristic detection assists triage and does not replace human verification with banks or vendors."
    )
    return _build_pdf(
        f"Phishing Analysis Report (#{record.id})",
        business_name,
        record.created_at.isoformat(),
        summary,
        sections,
        limitation,
    )


def generate_url_pdf(record: Any, business_name: str) -> bytes:
    tls = getattr(record, "tls_info", None) or {}
    summary = [
        ["Submitted URL", record.submitted_url],
        ["Normalized Host", record.normalized_host],
        ["Verdict Class", getattr(record, "verdict_classification", "Unknown")],
        ["Risk Score", f"{record.risk_score} / 100 ({record.risk_category})"],
        ["Analysis Engine", record.reputation_source],
        ["SPF / DMARC DNS", f"SPF={record.dns_records.get('spf_present', False)}, DMARC={record.dns_records.get('dmarc_present', False)}"],
        ["TLS Certificate", f"{tls.get('tls_status', 'n/a')} ({tls.get('issuer_org') or 'No issuer metadata'})"],
    ]
    ind_items = [
        f"[{i.get('severity', 'info').upper()}] {i.get('label', '')}: {i.get('detail', '')}"
        for i in (record.indicators or [])
    ]
    sections = [
        {"heading": "Technical Explanation", "text": record.technical_explanation},
        {"heading": "Detected Indicators", "items": ind_items or ["No high-risk indicators found."]},
        {"heading": "Security Recommendations", "items": record.recommendations or []},
    ]
    limitation = (
        "SafePulse AI never fetches, renders, or executes submitted URLs to prevent SSRF and malware exposure. "
        "Low risk means no local red flags were detected; it does not certify a website as safe."
    )
    return _build_pdf(
        f"URL Security Analysis Report (#{record.id})",
        business_name,
        record.created_at.isoformat(),
        summary,
        sections,
        limitation,
    )


def generate_assessment_pdf(record: Any, business_name: str) -> bytes:
    summary = [
        ["Overall Security Score", f"{record.overall_score} / 100 ({record.security_category})"],
        ["Weak Areas Count", str(len(record.weak_areas or []))],
        ["Critical Gaps Count", str(len(record.critical_gaps or []))],
        ["Last Updated", record.updated_at.isoformat()],
    ]
    domain_lines = [f"{k.replace('_', ' ').title()}: {v}%" for k, v in (record.category_scores or {}).items()]
    rec_lines = [
        f"[{r.get('priority', 'Medium')}] {r.get('domain_label', '')}: {r.get('action', '')}"
        for r in (record.recommendations or [])
    ]
    sections = [
        {"heading": "Domain Scores (10 Controls)", "items": domain_lines},
        {"heading": "Critical Gaps", "items": record.critical_gaps or ["None reported."]},
        {"heading": "Prioritized Action Plan (CERT-In MSME Aligned)", "items": rec_lines or ["Maintain current controls and review quarterly."]},
    ]
    limitation = (
        "This assessment reflects self-reported business security practices against CERT-In MSME guidance and does not constitute a formal penetration test or regulatory audit."
    )
    return _build_pdf(
        f"Business Security Assessment Report (#{record.id})",
        business_name,
        record.updated_at.isoformat(),
        summary,
        sections,
        limitation,
    )


def generate_incident_pdf(record: Any, business_name: str) -> bytes:
    items = record.checklist_items or []
    completed = sum(1 for i in items if i.is_completed)
    summary = [
        ["Incident Scenario", record.title],
        ["Severity", record.severity],
        ["Status", record.status],
        ["Assigned Owner", getattr(record, "assigned_to", None) or "Unassigned"],
        ["Checklist Progress", f"{completed} of {len(items)} steps completed"],
        ["Opened At", record.created_at.isoformat()],
    ]
    checklist_lines = [
        f"[{'DONE' if i.is_completed else 'OPEN'}] ({i.phase}) {i.title} — {i.guidance}"
        for i in items
    ]
    timeline_lines = [
        f"[{n.created_at.strftime('%Y-%m-%d %H:%M UTC')}] {n.author_name} ({n.event_type}): {n.content}"
        for n in (getattr(record, "timeline_notes", None) or [])
    ]
    sections = [
        {"heading": "Incident Context & Notes", "text": record.notes or "No additional incident notes recorded."},
        {"heading": "Resolution Summary", "text": getattr(record, "resolution_summary", None) or "Incident resolution summary pending."},
        {"heading": "Guided Response Checklist", "items": checklist_lines},
        {"heading": "Evidence & Activity Timeline", "items": timeline_lines or ["No manual timeline notes added yet."]},
    ]
    limitation = (
        "SafePulse AI provides structured response guidance only. It cannot independently remove malware, freeze bank transfers, recover hacked accounts, or guarantee incident resolution."
    )
    return _build_pdf(
        f"Incident Response Checklist (#{record.id})",
        business_name,
        record.updated_at.isoformat(),
        summary,
        sections,
        limitation,
    )


def generate_monthly_security_pdf(report_data: Dict[str, Any], business_name: str) -> bytes:
    summary = [
        ["Workspace", business_name],
        ["Subscription Tier", str(report_data.get("subscription_tier", "free")).upper()],
        ["Business Health Score", f"{report_data.get('security_score', 'Not Assessed')} ({report_data.get('security_category', 'N/A')})"],
        ["Threats Scanned (Period)", str(report_data.get("total_analyses", 0))],
        ["High / Critical Findings", str(report_data.get("high_risk_findings", 0))],
        ["Team MFA Adoption", f"{report_data.get('mfa_adoption_percent', 0)}% ({report_data.get('mfa_enabled_count', 0)}/{report_data.get('team_count', 0)} staff)"],
        ["Controls Completed", f"{report_data.get('controls_completed', 0)}/{report_data.get('controls_total', 0)} verified"],
        ["Incidents (Active / Total)", f"{report_data.get('active_incidents', 0)} / {report_data.get('total_incidents', 0)}"],
    ]
    sections = [
        {
            "heading": "Executive Security Summary",
            "text": report_data.get("executive_summary", ""),
        },
        {
            "heading": "Top Threat Findings & Critical Assessment Gaps",
            "items": report_data.get("top_risks") or ["No critical findings recorded during this period."],
        },
        {
            "heading": "30-Day Security Improvement Roadmap",
            "items": report_data.get("roadmap_items") or ["Maintain weekly backups, enforce 2FA on all accounts, and run staff phishing drills."],
        },
    ]
    limitation = (
        "This monthly executive summary reflects scans, assessments, incident checklists, and manually verified governance controls stored inside SafePulse AI. "
        "It does not represent automated live endpoint EDR telemetry unless external integrations are explicitly connected."
    )
    return _build_pdf(
        "Monthly Business Security Executive Report",
        business_name,
        report_data.get("generated_at", ""),
        summary,
        sections,
        limitation,
    )

