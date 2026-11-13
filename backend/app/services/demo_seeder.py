
from __future__ import annotations

from sqlalchemy.orm import Session

from ..ml.predictor import analyze_message
from ..models import (
    AssessmentAnswer,
    AwarenessQuiz,
    Business,
    BusinessMember,
    Incident,
    IncidentChecklistItem,
    IncidentNote,
    PhishingAnalysis,
    SecurityAssessment,
    URLScan,
    User,
)
from ..security import hash_password, record_audit_log
from .assessment_engine import evaluate_assessment
from .awareness_engine import QUIZ_DEFINITIONS
from .governance_engine import DEFAULT_CONTROLS
from .incident_engine import get_scenario_steps


DEMO_EMAIL = "demo@safepulseai.org"

HACKATHON_SAMPLE_MESSAGES = [
    {
        "id": "demo-bank-kyc",
        "label": "Scenario 1 (Demo): Bank Account Verification Scam",
        "channel": "sms",
        "sender_hint": "VK-SBIALT",
        "message": (
            "URGENT: Your SBI corporate bank account will be suspended within 2 hours due to incomplete KYC. "
            "Verify your PAN, netbanking password, and OTP immediately at http://sbi-kyc-verify-portal.xyz/login"
        ),
    },
    {
        "id": "demo-whatsapp-boss",
        "label": "Demo: WhatsApp Owner Impersonation Scam",
        "channel": "whatsapp",
        "sender_hint": "+91-98765-00112 (Unknown)",
        "message": (
            "Hi, this is the pharmacy owner speaking from my new WhatsApp number. I am stuck in a hospital meeting, "
            "do not call me. Transfer Rs 25,000 urgently to supplier UPI quickpay88@ybl right now."
        ),
    },
    {
        "id": "demo-gst-notice",
        "label": "Demo: Fake GST Penalty Notice Email",
        "channel": "email",
        "sender_hint": "gst-alerts@gmail.com",
        "message": (
            "FINAL NOTICE: Your business GSTIN registration faces cancellation for mismatch in GSTR-3B. "
            "Pay penalty Rs 4,850 within 24 hours at http://gst-portal-pay.click/penalty to avoid shop sealing."
        ),
    },
    {
        "id": "demo-legit-invoice",
        "label": "Demo: Legitimate Supplier Invoice (Low Risk)",
        "channel": "email",
        "sender_hint": "accounts@medplusdistributors.in",
        "message": (
            "Hi Priya, attached is our monthly medicine supply invoice #INV-2026-0412 for Rs 32,450 as discussed on yesterday's call. "
            "Payment terms remain Net 15 to our registered bank account on file."
        ),
    },
]

HACKATHON_SAMPLE_URLS = [
    {
        "id": "demo-phish-url",
        "label": "Scenario 2 (Demo): Suspicious Lookalike Bank URL",
        "url": "http://sbi-kyc-verify-portal.xyz/netbanking/login?verify=otp",
    },
    {
        "id": "demo-shortener-url",
        "label": "Demo: Obfuscated Shortener Link",
        "url": "https://bit.ly/gst-refund-claim-now",
    },
    {
        "id": "demo-official-url",
        "label": "Demo: Official Government GST Portal",
        "url": "https://www.gst.gov.in/",
    },
]


def ensure_quizzes_seeded(db: Session) -> None:
    for q in QUIZ_DEFINITIONS:
        exists = db.query(AwarenessQuiz).filter(AwarenessQuiz.slug == q["slug"]).first()
        if not exists:
            db.add(
                AwarenessQuiz(
                    slug=q["slug"],
                    title=q["title_en"],
                    topic=q["topic"],
                    difficulty=q["difficulty"],
                    questions_count=len(q["questions"]),
                )
            )
    db.commit()


def ensure_demo_workspace(db: Session) -> User:
    """Create or return the dedicated Demo Mode user with clearly labeled sample records."""
    ensure_quizzes_seeded(db)

    demo_user = db.query(User).filter(User.email == DEMO_EMAIL).first()
    if demo_user:
        return demo_user

    demo_user = User(
        email=DEMO_EMAIL,
        full_name="Priya Das (Demo Owner)",
        password_hash=hash_password("DemoShield2026!"),
        role="owner",
        preferred_language="en",
        is_demo=True,
    )
    db.add(demo_user)
    db.commit()
    db.refresh(demo_user)

    demo_biz = Business(
        owner_id=demo_user.id,
        name="Brahmaputra Care Pharmacy (Demo)",
        industry="Pharmacy & Healthcare Retail",
        employee_count=12,
        city="Guwahati",
        primary_email_domain="brahmaputracare-demo.in",
        is_demo_workspace=True,
    )
    db.add(demo_biz)
    db.commit()
    db.refresh(demo_biz)

    # Seed realistic clearly labeled demo phishing analyses using the real ML predictor
    for sample in HACKATHON_SAMPLE_MESSAGES[:3]:
        res = analyze_message(
            message=sample["message"],
            channel=sample["channel"],
            sender_hint=sample["sender_hint"],
            language="en",
        )
        db.add(
            PhishingAnalysis(
                business_id=demo_biz.id,
                user_id=demo_user.id,
                channel=res["channel"],
                sender_hint=res["sender_hint"],
                message_excerpt=res["message_excerpt"],
                raw_message=res["raw_message"],
                risk_score=res["risk_score"],
                risk_category=res["risk_category"],
                ml_probability=res["ml_probability"],
                model_confidence=res["model_confidence"],
                highlighted_phrases=res["highlighted_phrases"],
                social_engineering_tactics=res["social_engineering_tactics"],
                reasons=res["reasons"],
                recommendations=res["recommendations"],
                is_demo_sample=True,
            )
        )

    # Seed clearly labeled demo URL scans (without live network blocking issues in case offline, using static + safe dns)
    from .url_analyzer import analyze_url

    for url_sample in [
        "http://sbi-kyc-verify-portal.xyz/netbanking/login?verify=otp",
        "https://bit.ly/gst-refund-claim-now",
        "https://gst.gov.in/",
    ]:
        u_res = analyze_url(url_sample, language="en")
        db.add(
            URLScan(
                business_id=demo_biz.id,
                user_id=demo_user.id,
                submitted_url=u_res["submitted_url"],
                normalized_host=u_res["normalized_host"],
                scheme=u_res["scheme"],
                risk_score=u_res["risk_score"],
                risk_category=u_res["risk_category"],
                verdict_classification=u_res["verdict_classification"],
                indicators=u_res["indicators"],
                dns_records=u_res["dns_records"],
                tls_info=u_res["tls_info"],
                reputation_source=u_res["reputation_source"],
                technical_explanation=u_res["technical_explanation"],
                recommendations=u_res["recommendations"],
                is_demo_sample=True,
            )
        )

    # Seed Demo Scenario 3 assessment
    demo_answers = {
        "passwords": "partial",
        "mfa": "no",
        "email_security": "partial",
        "access_control": "yes",
        "updates": "yes",
        "backups": "partial",
        "data_protection": "partial",
        "device_security": "yes",
        "wifi_security": "no",
        "incident_readiness": "no",
    }
    eval_res = evaluate_assessment(demo_answers, language="en")
    assessment = SecurityAssessment(
        business_id=demo_biz.id,
        user_id=demo_user.id,
        overall_score=eval_res["overall_score"],
        security_category=eval_res["security_category"],
        category_scores=eval_res["category_scores"],
        weak_areas=eval_res["weak_areas"],
        critical_gaps=eval_res["critical_gaps"],
        recommendations=eval_res["recommendations"],
        is_demo_sample=True,
    )
    db.add(assessment)
    db.flush()
    for row in eval_res["answer_rows"]:
        db.add(AssessmentAnswer(assessment_id=assessment.id, **row))

    # Seed Demo Scenario 4 incident checklist
    scen = get_scenario_steps("phishing_link_clicked")
    incident = Incident(
        business_id=demo_biz.id,
        user_id=demo_user.id,
        scenario_key=scen.key,
        title=f"{scen.title_en} (Demo Scenario)",
        severity=scen.severity,
        status="in_progress",
        assigned_to="Priya Das (Demo Owner)",
        notes="Demo Scenario 4: Counter staff clicked a fake bank KYC link on billing browser.",
        is_demo_sample=True,
    )
    db.add(incident)
    db.flush()
    for idx, step in enumerate(scen.steps):
        db.add(
            IncidentChecklistItem(
                incident_id=incident.id,
                phase=step.phase,
                title=step.title_en,
                guidance=step.guidance_en,
                is_completed=(idx < 2),
                sort_order=idx,
            )
        )
    db.add(
        IncidentNote(
            incident_id=incident.id,
            author_name="Priya Das (Demo Owner)",
            event_type="incident_opened",
            content="Opened Demo Scenario 4 after counter PC flagged suspicious bank KYC redirect.",
        )
    )

    # Seed Demo Team & MFA Directory (showing partial MFA adoption gap)
    demo_team = [
        ("Priya Das", "priya@brahmaputracare-demo.in", "owner", "Management", True, True),
        ("Bikash Sarma", "bikash@brahmaputracare-demo.in", "manager", "Inventory & Billing", True, True),
        ("Ananya Kalita", "ananya@brahmaputracare-demo.in", "staff", "Front Counter POS", False, True),
        ("Rituraj Bora", "rituraj@brahmaputracare-demo.in", "staff", "Delivery & Accounts", False, False),
    ]
    for name, email, role, dept, mfa, trained in demo_team:
        db.add(
            BusinessMember(
                business_id=demo_biz.id,
                full_name=name,
                email=email,
                role=role,
                department=dept,
                mfa_enabled=mfa,
                awareness_trained=trained,
            )
        )

    from ..models import BusinessControl

    for idx, item in enumerate(DEFAULT_CONTROLS):
        db.add(
            BusinessControl(
                business_id=demo_biz.id,
                category=item["category"],
                control_key=item["control_key"],
                title=item["title_en"],
                guidance=item["guidance_en"],
                priority=item["priority"],
                is_completed=(idx % 3 == 0),
                owner_name="Priya Das" if idx % 3 == 0 else None,
            )
        )

    db.commit()
    record_audit_log(
        db=db,
        action="demo.initialized",
        resource_type="business",
        resource_id=str(demo_biz.id),
        summary="Initialized clearly labeled Demo Mode workspace for hackathon exploration.",
        user_id=demo_user.id,
        business_id=demo_biz.id,
    )
    return demo_user
