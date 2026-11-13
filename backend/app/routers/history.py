"""Unified Scan History and Audit Logs API routes."""

from __future__ import annotations

from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import AuditLog, Incident, PhishingAnalysis, SecurityAssessment, URLScan
from ..security import get_current_business, record_audit_log


router = APIRouter(prefix="/api/history", tags=["Scan History"])


@router.get("/unified")
def get_unified_history(ctx=Depends(get_current_business), db: Session = Depends(get_db)) -> Dict[str, Any]:
    _, business = ctx

    phishing = (
        db.query(PhishingAnalysis)
        .filter(PhishingAnalysis.business_id == business.id)
        .order_by(PhishingAnalysis.created_at.desc())
        .limit(50)
        .all()
    )
    urls = (
        db.query(URLScan)
        .filter(URLScan.business_id == business.id)
        .order_by(URLScan.created_at.desc())
        .limit(50)
        .all()
    )
    assessments = (
        db.query(SecurityAssessment)
        .filter(SecurityAssessment.business_id == business.id)
        .order_by(SecurityAssessment.created_at.desc())
        .limit(30)
        .all()
    )
    incidents = (
        db.query(Incident)
        .filter(Incident.business_id == business.id)
        .order_by(Incident.created_at.desc())
        .limit(30)
        .all()
    )

    items: List[Dict[str, Any]] = []
    for p in phishing:
        items.append(
            {
                "uid": f"phishing-{p.id}",
                "record_id": p.id,
                "type": "phishing",
                "title": f"{p.channel.upper()} Message Scan",
                "target": p.message_excerpt,
                "score": p.risk_score,
                "status_label": p.risk_category,
                "is_demo_sample": p.is_demo_sample,
                "created_at": p.created_at.isoformat(),
                "pdf_url": f"/api/phishing/{p.id}/report.pdf",
            }
        )
    for u in urls:
        items.append(
            {
                "uid": f"url-{u.id}",
                "record_id": u.id,
                "type": "url",
                "title": f"URL Scan ({u.normalized_host})",
                "target": u.submitted_url,
                "score": u.risk_score,
                "status_label": u.risk_category,
                "is_demo_sample": u.is_demo_sample,
                "created_at": u.created_at.isoformat(),
                "pdf_url": f"/api/urls/{u.id}/report.pdf",
            }
        )
    for a in assessments:
        items.append(
            {
                "uid": f"assessment-{a.id}",
                "record_id": a.id,
                "type": "assessment",
                "title": "Business Security Assessment",
                "target": f"Score {a.overall_score}/100 ({len(a.critical_gaps or [])} critical gaps)",
                "score": a.overall_score,
                "status_label": a.security_category,
                "is_demo_sample": a.is_demo_sample,
                "created_at": a.created_at.isoformat(),
                "pdf_url": f"/api/assessments/{a.id}/report.pdf",
            }
        )
    for inc in incidents:
        done = sum(1 for c in inc.checklist_items if c.is_completed)
        total = len(inc.checklist_items)
        items.append(
            {
                "uid": f"incident-{inc.id}",
                "record_id": inc.id,
                "type": "incident",
                "title": inc.title,
                "target": f"{done}/{total} checklist actions completed",
                "score": int(round((done / total) * 100)) if total else 0,
                "status_label": inc.severity,
                "is_demo_sample": inc.is_demo_sample,
                "created_at": inc.created_at.isoformat(),
                "pdf_url": f"/api/incidents/{inc.id}/report.pdf",
            }
        )

    items.sort(key=lambda x: x["created_at"], reverse=True)
    return {"items": items}


@router.get("/audit-logs")
def get_audit_logs(ctx=Depends(get_current_business), db: Session = Depends(get_db)):
    _, business = ctx
    logs = (
        db.query(AuditLog)
        .filter(AuditLog.business_id == business.id)
        .order_by(AuditLog.created_at.desc())
        .limit(60)
        .all()
    )
    return {
        "logs": [
            {
                "id": l.id,
                "action": l.action,
                "resource_type": l.resource_type,
                "resource_id": l.resource_id,
                "summary": l.summary,
                "created_at": l.created_at.isoformat(),
            }
            for l in logs
        ]
    }


@router.delete("/{record_type}/{record_id}")
def delete_history_item(
    record_type: str,
    record_id: int,
    request: Request,
    ctx=Depends(get_current_business),
    db: Session = Depends(get_db),
):
    user, business = ctx
    model_map = {
        "phishing": PhishingAnalysis,
        "url": URLScan,
        "assessment": SecurityAssessment,
        "incident": Incident,
    }
    model_cls = model_map.get(record_type)
    if not model_cls:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported record type.")

    row = (
        db.query(model_cls)
        .filter(model_cls.id == record_id, model_cls.business_id == business.id)
        .first()
    )
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found.")

    db.delete(row)
    db.commit()
    record_audit_log(
        db=db,
        action=f"{record_type}.deleted",
        resource_type=record_type,
        resource_id=str(record_id),
        summary=f"Deleted {record_type} record #{record_id}.",
        user_id=user.id,
        business_id=business.id,
        request=request,
    )
    return {"status": "deleted"}

