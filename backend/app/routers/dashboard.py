"""Main Overview Dashboard API aggregating real database records for the active business."""

from __future__ import annotations

from collections import Counter
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import (
    BusinessControl,
    BusinessMember,
    Incident,
    PhishingAnalysis,
    QuizResult,
    SecurityAssessment,
    URLScan,
)
from ..security import get_current_business
from .governance import compute_monthly_usage, ensure_default_controls_seeded


router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("/overview")
def get_dashboard_overview(
    language: str = Query("en", pattern="^(en|bn)$"),
    days: Optional[int] = Query(None, ge=1, le=3650),
    ctx=Depends(get_current_business),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    user, business = ctx
    cutoff = (datetime.now(timezone.utc) - timedelta(days=days)) if days else None

    phishing_q = db.query(PhishingAnalysis).filter(PhishingAnalysis.business_id == business.id)
    url_q = db.query(URLScan).filter(URLScan.business_id == business.id)
    assess_q = db.query(SecurityAssessment).filter(SecurityAssessment.business_id == business.id)
    inc_q = db.query(Incident).filter(Incident.business_id == business.id)

    if cutoff is not None:
        phishing_q = phishing_q.filter(PhishingAnalysis.created_at >= cutoff)
        url_q = url_q.filter(URLScan.created_at >= cutoff)
        assess_q = assess_q.filter(SecurityAssessment.created_at >= cutoff)
        inc_q = inc_q.filter(Incident.created_at >= cutoff)

    phishing_rows = phishing_q.order_by(PhishingAnalysis.created_at.desc()).all()
    url_rows = url_q.order_by(URLScan.created_at.desc()).all()
    assessments = assess_q.order_by(SecurityAssessment.created_at.asc()).all()
    incidents = inc_q.order_by(Incident.updated_at.desc()).all()
    quiz_results = (
        db.query(QuizResult)
        .filter(QuizResult.business_id == business.id, QuizResult.user_id == user.id)
        .all()
    )
    members = db.query(BusinessMember).filter(BusinessMember.business_id == business.id).all()
    controls = ensure_default_controls_seeded(db, business.id, language=language)

    latest_assessment = assessments[-1] if assessments else None
    business_security_score = latest_assessment.overall_score if latest_assessment else None
    security_category = latest_assessment.security_category if latest_assessment else "Not Assessed"

    total_threat_analyses = len(phishing_rows) + len(url_rows)
    high_risk_findings = sum(
        1 for p in phishing_rows if p.risk_category in ("High Risk", "Critical Risk")
    ) + sum(1 for u in url_rows if u.risk_category in ("High Risk", "Critical Risk"))

    band_counts = Counter({"Low Risk": 0, "Moderate Risk": 0, "High Risk": 0, "Critical Risk": 0})
    for p in phishing_rows:
        band_counts[p.risk_category] += 1
    for u in url_rows:
        band_counts[u.risk_category] += 1

    risk_distribution = [
        {"name": "Low Risk", "count": band_counts["Low Risk"], "color": "#22C55E"},
        {"name": "Moderate Risk", "count": band_counts["Moderate Risk"], "color": "#F59E0B"},
        {"name": "High Risk", "count": band_counts["High Risk"], "color": "#FB923C"},
        {"name": "Critical Risk", "count": band_counts["Critical Risk"], "color": "#EF4444"},
    ]

    # Security score history from actual assessments; if multiple or single assessment, plot actual timeline
    score_trend: List[Dict[str, Any]] = [
        {
            "label": a.created_at.strftime("%b %d %H:%M"),
            "score": a.overall_score,
            "category": a.security_category,
        }
        for a in assessments[-8:]
    ]

    # Build actionable recommendations grounded in real DB state
    recommendations: List[Dict[str, str]] = []
    if latest_assessment and latest_assessment.recommendations:
        for rec in latest_assessment.recommendations[:3]:
            recommendations.append(
                {
                    "source": "Assessment",
                    "priority": rec.get("priority", "Medium"),
                    "title": rec.get("domain_label", "Security Control"),
                    "detail": rec.get("action", ""),
                }
            )
    else:
        recommendations.append(
            {
                "source": "Assessment",
                "priority": "High",
                "title": "বিজনেস সিকিউরিটি চেক সম্পন্ন করুন" if language == "bn" else "Complete Business Security Health Check",
                "detail": (
                    "আপনার ব্যবসার ১০টি প্রধান নিরাপত্তা ঝুঁকি মাপতে প্রথম অ্যাসেসমেন্ট সম্পন্ন করুন।"
                    if language == "bn"
                    else "Run your 10-domain CERT-In MSME aligned health check to establish your baseline score."
                ),
            }
        )

    if high_risk_findings > 0:
        recommendations.append(
            {
                "source": "Threat Monitor",
                "priority": "Critical",
                "title": "উচ্চ-ঝুঁকির ফিশিং/URL সতর্কতা পর্যালোচনা করুন" if language == "bn" else f"Review {high_risk_findings} High/Critical Threat Finding(s)",
                "detail": (
                    "কোনো কর্মী সন্দেহজনক লিঙ্কে ক্লিক করে থাকলে অবিলম্বে ইনসিডেন্ট রেসপন্স চেকলিস্ট শুরু করুন।"
                    if language == "bn"
                    else "Ensure no staff clicked flagged links or shared OTPs; open an Incident Playbook immediately if exposure occurred."
                ),
            }
        )

    if not quiz_results:
        recommendations.append(
            {
                "source": "Awareness",
                "priority": "Medium",
                "title": "কর্মীদের সাইবার সচেতনতা কুইজ শুরু করুন" if language == "bn" else "Complete Staff Cyber Awareness Training",
                "detail": (
                    "UPI PIN প্রতারণা ও হোয়াটসঅ্যাপ স্ক্যাম চিনতে টিমের জন্য প্রশিক্ষণ কুইজ সম্পন্ন করুন।"
                    if language == "bn"
                    else "Have staff complete the interactive phishing & UPI safety quiz to reduce social engineering risk."
                ),
            }
        )

    recent_phishing = [
        {
            "id": p.id,
            "channel": p.channel,
            "excerpt": p.message_excerpt,
            "risk_score": p.risk_score,
            "risk_category": p.risk_category,
            "is_demo_sample": p.is_demo_sample,
            "created_at": p.created_at.isoformat(),
        }
        for p in phishing_rows[:5]
    ]
    recent_urls = [
        {
            "id": u.id,
            "url": u.submitted_url,
            "host": u.normalized_host,
            "risk_score": u.risk_score,
            "risk_category": u.risk_category,
            "is_demo_sample": u.is_demo_sample,
            "created_at": u.created_at.isoformat(),
        }
        for u in url_rows[:5]
    ]
    incident_activity = [
        {
            "id": inc.id,
            "title": inc.title,
            "severity": inc.severity,
            "status": inc.status,
            "completed_count": sum(1 for item in inc.checklist_items if item.is_completed),
            "total_count": len(inc.checklist_items),
            "is_demo_sample": inc.is_demo_sample,
            "updated_at": inc.updated_at.isoformat(),
        }
        for inc in incidents[:5]
    ]

    is_empty = (
        days is None
        and total_threat_analyses == 0
        and len(assessments) == 0
        and len(incidents) == 0
    )

    channel_counts = Counter(p.channel.upper() for p in phishing_rows)
    if url_rows:
        channel_counts["URL"] = len(url_rows)
    threat_vectors = [
        {"channel": ch, "count": cnt}
        for ch, cnt in channel_counts.most_common()
    ]

    mfa_enabled_count = sum(1 for m in members if m.mfa_enabled)
    mfa_adoption_pct = int(round((mfa_enabled_count / len(members)) * 100)) if members else 0
    controls_completed = sum(1 for c in controls if c.is_completed)
    controls_pct = int(round((controls_completed / len(controls)) * 100)) if controls else 0
    resolved_incidents = sum(1 for i in incidents if i.status == "resolved")
    incident_resolution_pct = int(round((resolved_incidents / len(incidents)) * 100)) if incidents else 0
    score_delta = (
        (assessments[-1].overall_score - assessments[0].overall_score)
        if len(assessments) >= 2
        else 0
    )
    monthly_used = compute_monthly_usage(db, business.id)

    return {
        "business": {
            "id": business.id,
            "name": business.name,
            "industry": business.industry,
            "city": business.city,
            "is_demo_workspace": business.is_demo_workspace,
            "subscription_tier": business.subscription_tier,
        },
        "is_empty": is_empty,
        "summary": {
            "business_security_score": business_security_score,
            "security_category": security_category,
            "total_threat_analyses": total_threat_analyses,
            "high_risk_findings": high_risk_findings,
            "completed_assessments": len(assessments),
            "active_incidents": sum(1 for i in incidents if i.status != "resolved"),
            "quizzes_completed": len(quiz_results),
        },
        "improvement_progress": {
            "assessment_score_delta": score_delta,
            "mfa_adoption_percent": mfa_adoption_pct,
            "mfa_enabled_count": mfa_enabled_count,
            "team_count": len(members),
            "controls_completed": controls_completed,
            "controls_total": len(controls),
            "controls_percent": controls_pct,
            "incident_resolution_percent": incident_resolution_pct,
        },
        "subscription_usage": {
            "tier": business.subscription_tier,
            "monthly_scans_used": monthly_used,
            "monthly_scan_quota": business.monthly_scan_quota,
        },
        "threat_vectors": threat_vectors,
        "score_trend": score_trend,
        "risk_distribution": risk_distribution,
        "recent_phishing": recent_phishing,
        "recent_urls": recent_urls,
        "recommendations": recommendations[:4],
        "incident_activity": incident_activity,
    }

