"""Business governance, team MFA, controls, future integrations, and monthly PDF reports."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi.responses import Response
from sqlalchemy.orm import Session

from ..config import settings
from ..database import get_db
from ..models import (
    BusinessControl,
    BusinessMember,
    Incident,
    IntegrationConfig,
    PhishingAnalysis,
    SecurityAssessment,
    URLScan,
)
from ..schemas import (
    BusinessControlOut,
    BusinessControlUpdateRequest,
    BusinessMemberCreateRequest,
    BusinessMemberOut,
    BusinessMemberUpdateRequest,
    IntegrationUpdateRequest,
)
from ..security import enforce_rate_limit, get_current_business, record_audit_log
from ..services.governance_engine import (
    DEFAULT_CONTROLS,
    INTEGRATION_CATALOG,
    SUBSCRIPTION_PLANS,
)
from ..services.pdf_report import generate_monthly_security_pdf


router = APIRouter(tags=["Governance & Reporting"])


def ensure_default_controls_seeded(db: Session, business_id: int, language: str = "en") -> List[BusinessControl]:
    existing = (
        db.query(BusinessControl)
        .filter(BusinessControl.business_id == business_id)
        .order_by(BusinessControl.id.asc())
        .all()
    )
    if existing:
        return existing

    created: List[BusinessControl] = []
    for item in DEFAULT_CONTROLS:
        row = BusinessControl(
            business_id=business_id,
            category=item["category"],
            control_key=item["control_key"],
            title=item["title_bn"] if language == "bn" else item["title_en"],
            guidance=item["guidance_bn"] if language == "bn" else item["guidance_en"],
            priority=item["priority"],
            is_completed=False,
        )
        db.add(row)
        created.append(row)
    db.commit()
    for row in created:
        db.refresh(row)
    return created


def compute_monthly_usage(db: Session, business_id: int) -> int:
    now = datetime.now(timezone.utc)
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    phish_count = (
        db.query(PhishingAnalysis)
        .filter(PhishingAnalysis.business_id == business_id, PhishingAnalysis.created_at >= month_start)
        .count()
    )
    url_count = (
        db.query(URLScan)
        .filter(URLScan.business_id == business_id, URLScan.created_at >= month_start)
        .count()
    )
    return phish_count + url_count


@router.get("/api/governance/overview")
def get_governance_overview(
    language: str = Query("en", pattern="^(en|bn)$"),
    ctx=Depends(get_current_business),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    _user, business = ctx
    controls = ensure_default_controls_seeded(db, business.id, language=language)
    members = (
        db.query(BusinessMember)
        .filter(BusinessMember.business_id == business.id)
        .order_by(BusinessMember.created_at.asc())
        .all()
    )
    configs = {
        c.provider_key: c
        for c in db.query(IntegrationConfig).filter(IntegrationConfig.business_id == business.id).all()
    }

    total_members = len(members)
    mfa_count = sum(1 for m in members if m.mfa_enabled)
    trained_count = sum(1 for m in members if m.awareness_trained)
    mfa_pct = int(round((mfa_count / total_members) * 100)) if total_members else 0

    completed_controls = sum(1 for c in controls if c.is_completed)
    controls_pct = int(round((completed_controls / len(controls)) * 100)) if controls else 0

    integrations: List[Dict[str, Any]] = []
    for entry in INTEGRATION_CATALOG:
        cfg = configs.get(entry["provider_key"])
        is_live_intel = (
            entry["provider_key"] == "google_safe_browsing"
            and bool(settings.google_safe_browsing_api_key)
        )
        if is_live_intel:
            runtime_status = "active_server_env"
        elif cfg and cfg.enabled:
            runtime_status = "configured_awaiting_oauth_gateway"
        else:
            runtime_status = "unconfigured"
        integrations.append(
            {
                **entry,
                "enabled": bool(cfg.enabled) if cfg else is_live_intel,
                "endpoint_or_account": cfg.endpoint_or_account if cfg else None,
                "notes": cfg.notes if cfg else None,
                "runtime_status": runtime_status,
                "updated_at": cfg.updated_at.isoformat() if cfg else None,
            }
        )

    plan_info = SUBSCRIPTION_PLANS.get(business.subscription_tier, SUBSCRIPTION_PLANS["free"])
    monthly_used = compute_monthly_usage(db, business.id)

    return {
        "mfa_stats": {
            "total_members": total_members,
            "mfa_enabled_count": mfa_count,
            "mfa_adoption_percent": mfa_pct,
            "awareness_trained_count": trained_count,
        },
        "controls_stats": {
            "completed_count": completed_controls,
            "total_count": len(controls),
            "completion_percent": controls_pct,
        },
        "members": [
            BusinessMemberOut(
                id=m.id,
                full_name=m.full_name,
                email=m.email,
                role=m.role,
                department=m.department,
                mfa_enabled=m.mfa_enabled,
                awareness_trained=m.awareness_trained,
                created_at=m.created_at,
            )
            for m in members
        ],
        "controls": [
            BusinessControlOut(
                id=c.id,
                category=c.category,
                control_key=c.control_key,
                title=c.title,
                guidance=c.guidance,
                priority=c.priority,
                is_completed=c.is_completed,
                owner_name=c.owner_name,
                target_date=c.target_date,
                last_verified_at=c.last_verified_at,
            )
            for c in controls
        ],
        "integrations": integrations,
        "subscription": {
            **plan_info,
            "monthly_scans_used": monthly_used,
            "monthly_scan_quota": business.monthly_scan_quota,
        },
        "available_plans": list(SUBSCRIPTION_PLANS.values()),
    }


@router.post("/api/governance/members", response_model=BusinessMemberOut, status_code=status.HTTP_201_CREATED)
def add_business_member(
    payload: BusinessMemberCreateRequest,
    request: Request,
    ctx=Depends(get_current_business),
    db: Session = Depends(get_db),
):
    enforce_rate_limit(request, bucket_suffix="gov_member_add", limit=40)
    user, business = ctx
    member = BusinessMember(
        business_id=business.id,
        full_name=payload.full_name.strip(),
        email=payload.email.lower().strip(),
        role=payload.role,
        department=payload.department.strip(),
        mfa_enabled=payload.mfa_enabled,
        awareness_trained=payload.awareness_trained,
    )
    db.add(member)
    db.commit()
    db.refresh(member)

    record_audit_log(
        db=db,
        action="governance.member_added",
        resource_type="business_member",
        resource_id=str(member.id),
        summary=f"Added team member '{member.full_name}' ({member.role}, MFA={'ON' if member.mfa_enabled else 'OFF'}).",
        user_id=user.id,
        business_id=business.id,
        request=request,
    )
    return member


@router.patch("/api/governance/members/{member_id}", response_model=BusinessMemberOut)
def update_business_member(
    member_id: int,
    payload: BusinessMemberUpdateRequest,
    request: Request,
    ctx=Depends(get_current_business),
    db: Session = Depends(get_db),
):
    user, business = ctx
    member = (
        db.query(BusinessMember)
        .filter(BusinessMember.id == member_id, BusinessMember.business_id == business.id)
        .first()
    )
    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team member not found.")

    if payload.role is not None:
        member.role = payload.role
    if payload.department is not None:
        member.department = payload.department.strip()
    if payload.mfa_enabled is not None:
        member.mfa_enabled = payload.mfa_enabled
    if payload.awareness_trained is not None:
        member.awareness_trained = payload.awareness_trained
    db.commit()
    db.refresh(member)

    record_audit_log(
        db=db,
        action="governance.member_updated",
        resource_type="business_member",
        resource_id=str(member.id),
        summary=f"Updated team member '{member.full_name}' (MFA={'ON' if member.mfa_enabled else 'OFF'}).",
        user_id=user.id,
        business_id=business.id,
        request=request,
    )
    return member


@router.delete("/api/governance/members/{member_id}")
def delete_business_member(
    member_id: int,
    request: Request,
    ctx=Depends(get_current_business),
    db: Session = Depends(get_db),
):
    user, business = ctx
    member = (
        db.query(BusinessMember)
        .filter(BusinessMember.id == member_id, BusinessMember.business_id == business.id)
        .first()
    )
    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team member not found.")
    name = member.full_name
    db.delete(member)
    db.commit()
    record_audit_log(
        db=db,
        action="governance.member_removed",
        resource_type="business_member",
        resource_id=str(member_id),
        summary=f"Removed team member '{name}'.",
        user_id=user.id,
        business_id=business.id,
        request=request,
    )
    return {"status": "deleted"}


@router.patch("/api/governance/controls/{control_id}", response_model=BusinessControlOut)
def update_business_control(
    control_id: int,
    payload: BusinessControlUpdateRequest,
    request: Request,
    ctx=Depends(get_current_business),
    db: Session = Depends(get_db),
):
    user, business = ctx
    control = (
        db.query(BusinessControl)
        .filter(BusinessControl.id == control_id, BusinessControl.business_id == business.id)
        .first()
    )
    if not control:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Control checklist item not found.")

    if payload.is_completed is not None:
        control.is_completed = payload.is_completed
        control.last_verified_at = datetime.now(timezone.utc) if payload.is_completed else None
    if payload.owner_name is not None:
        control.owner_name = payload.owner_name.strip() or None
    if payload.target_date is not None:
        control.target_date = payload.target_date.strip() or None
    db.commit()
    db.refresh(control)

    record_audit_log(
        db=db,
        action="governance.control_updated",
        resource_type="business_control",
        resource_id=str(control.id),
        summary=f"{'Verified' if control.is_completed else 'Reopened'} {control.category} control '{control.control_key}'.",
        user_id=user.id,
        business_id=business.id,
        request=request,
    )
    return control


@router.put("/api/governance/integrations/{provider_key}")
def update_integration_config(
    provider_key: str,
    payload: IntegrationUpdateRequest,
    request: Request,
    ctx=Depends(get_current_business),
    db: Session = Depends(get_db),
):
    valid_keys = {i["provider_key"] for i in INTEGRATION_CATALOG}
    if provider_key not in valid_keys:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unknown integration provider key.")
    user, business = ctx
    cfg = (
        db.query(IntegrationConfig)
        .filter(IntegrationConfig.business_id == business.id, IntegrationConfig.provider_key == provider_key)
        .first()
    )
    if not cfg:
        cfg = IntegrationConfig(business_id=business.id, provider_key=provider_key)
        db.add(cfg)
    cfg.enabled = payload.enabled
    cfg.endpoint_or_account = payload.endpoint_or_account.strip() if payload.endpoint_or_account else None
    cfg.notes = payload.notes.strip() if payload.notes else None
    db.commit()
    db.refresh(cfg)

    record_audit_log(
        db=db,
        action="integration.configured",
        resource_type="integration_config",
        resource_id=provider_key,
        summary=f"Saved readiness settings for integration '{provider_key}' (enabled={cfg.enabled}).",
        user_id=user.id,
        business_id=business.id,
        request=request,
    )
    return {"status": "saved", "provider_key": provider_key, "enabled": cfg.enabled}


@router.get("/api/reports/monthly.pdf")
def download_monthly_security_report(
    ctx=Depends(get_current_business),
    db: Session = Depends(get_db),
):
    _user, business = ctx
    phishing_rows = (
        db.query(PhishingAnalysis)
        .filter(PhishingAnalysis.business_id == business.id)
        .order_by(PhishingAnalysis.created_at.desc())
        .all()
    )
    url_rows = (
        db.query(URLScan)
        .filter(URLScan.business_id == business.id)
        .order_by(URLScan.created_at.desc())
        .all()
    )
    latest_assessment = (
        db.query(SecurityAssessment)
        .filter(SecurityAssessment.business_id == business.id)
        .order_by(SecurityAssessment.created_at.desc())
        .first()
    )
    incidents = (
        db.query(Incident)
        .filter(Incident.business_id == business.id)
        .order_by(Incident.updated_at.desc())
        .all()
    )
    members = db.query(BusinessMember).filter(BusinessMember.business_id == business.id).all()
    controls = ensure_default_controls_seeded(db, business.id, "en")

    high_risk = [
        f"Phishing ({p.channel.upper()}): {p.message_excerpt[:100]} — Score {p.risk_score}/100 ({p.risk_category})"
        for p in phishing_rows
        if p.risk_category in ("High Risk", "Critical Risk")
    ][:5] + [
        f"URL ({u.normalized_host}): {u.verdict_classification} — Score {u.risk_score}/100"
        for u in url_rows
        if u.risk_category in ("High Risk", "Critical Risk")
    ][:5]
    if latest_assessment and latest_assessment.critical_gaps:
        high_risk.extend([f"Assessment Gap: {gap}" for gap in latest_assessment.critical_gaps[:4]])

    open_controls = [
        f"[{c.priority}] ({c.category.upper()}) {c.title}"
        for c in controls
        if not c.is_completed
    ][:6]

    mfa_enabled = sum(1 for m in members if m.mfa_enabled)
    mfa_pct = int(round((mfa_enabled / len(members)) * 100)) if members else 0
    controls_done = sum(1 for c in controls if c.is_completed)

    score_text = f"{latest_assessment.overall_score}/100" if latest_assessment else "Not Assessed"
    exec_summary = (
        f"During the active reporting period, {business.name} recorded {len(phishing_rows) + len(url_rows)} threat analyses "
        f"({len(phishing_rows)} message scans and {len(url_rows)} URL inspections). "
        f"Current business security assessment score is {score_text}, team MFA adoption stands at {mfa_pct}% "
        f"({mfa_enabled}/{len(members)} members), and {controls_done} of {len(controls)} governance controls are verified complete."
    )

    pdf_bytes = generate_monthly_security_pdf(
        {
            "subscription_tier": business.subscription_tier,
            "security_score": latest_assessment.overall_score if latest_assessment else "Not Assessed",
            "security_category": latest_assessment.security_category if latest_assessment else "Pending",
            "total_analyses": len(phishing_rows) + len(url_rows),
            "high_risk_findings": sum(1 for p in phishing_rows if p.risk_category in ("High Risk", "Critical Risk"))
            + sum(1 for u in url_rows if u.risk_category in ("High Risk", "Critical Risk")),
            "mfa_adoption_percent": mfa_pct,
            "mfa_enabled_count": mfa_enabled,
            "team_count": len(members),
            "controls_completed": controls_done,
            "controls_total": len(controls),
            "active_incidents": sum(1 for i in incidents if i.status != "resolved"),
            "total_incidents": len(incidents),
            "executive_summary": exec_summary,
            "top_risks": high_risk,
            "roadmap_items": open_controls,
            "generated_at": datetime.now(timezone.utc).isoformat(),
        },
        business.name,
    )
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="cybershield-monthly-report-{business.id}.pdf"'},
    )

