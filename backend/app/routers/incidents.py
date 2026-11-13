"""Cyber Incident Response Center API routes."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi.responses import Response
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Incident, IncidentChecklistItem, IncidentNote
from ..schemas import (
    ChecklistToggleRequest,
    IncidentChecklistItemOut,
    IncidentCreateRequest,
    IncidentNoteCreateRequest,
    IncidentNoteOut,
    IncidentOut,
    IncidentUpdateRequest,
)
from ..security import enforce_rate_limit, get_current_business, record_audit_log
from ..services.incident_engine import get_scenario_steps, list_scenarios
from ..services.pdf_report import generate_incident_pdf


router = APIRouter(prefix="/api/incidents", tags=["Incident Response"])


def _serialize_incident(inc: Incident) -> IncidentOut:
    items = inc.checklist_items or []
    notes = inc.timeline_notes or []
    total = len(items)
    completed = sum(1 for i in items if i.is_completed)
    pct = int(round((completed / total) * 100)) if total else 0
    return IncidentOut(
        id=inc.id,
        scenario_key=inc.scenario_key,
        title=inc.title,
        severity=inc.severity,
        status=inc.status,
        assigned_to=inc.assigned_to,
        resolution_summary=inc.resolution_summary,
        notes=inc.notes,
        progress_percent=pct,
        completed_count=completed,
        total_count=total,
        is_demo_sample=inc.is_demo_sample,
        created_at=inc.created_at,
        updated_at=inc.updated_at,
        checklist_items=[
            IncidentChecklistItemOut(
                id=i.id,
                phase=i.phase,
                title=i.title,
                guidance=i.guidance,
                is_completed=i.is_completed,
                completed_at=i.completed_at,
                sort_order=i.sort_order,
            )
            for i in items
        ],
        timeline_notes=[
            IncidentNoteOut(
                id=n.id,
                author_name=n.author_name,
                event_type=n.event_type,
                content=n.content,
                created_at=n.created_at,
            )
            for n in notes
        ],
    )


@router.get("/scenarios")
def get_incident_scenarios(language: str = Query("en", pattern="^(en|bn)$")):
    return {"scenarios": list_scenarios(language)}


@router.get("", response_model=List[IncidentOut])
def list_incidents(ctx=Depends(get_current_business), db: Session = Depends(get_db)):
    _, business = ctx
    rows = (
        db.query(Incident)
        .filter(Incident.business_id == business.id)
        .order_by(Incident.updated_at.desc())
        .all()
    )
    return [_serialize_incident(r) for r in rows]


@router.post("", response_model=IncidentOut, status_code=status.HTTP_201_CREATED)
def create_incident(
    payload: IncidentCreateRequest,
    request: Request,
    ctx=Depends(get_current_business),
    db: Session = Depends(get_db),
):
    enforce_rate_limit(request, bucket_suffix="incident_create", limit=30)
    user, business = ctx

    try:
        scen = get_scenario_steps(payload.scenario_key, language=payload.language)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc

    default_title = scen.title_bn if payload.language == "bn" else scen.title_en
    incident = Incident(
        business_id=business.id,
        user_id=user.id,
        scenario_key=scen.key,
        title=(payload.title or default_title).strip(),
        severity=scen.severity,
        status="in_progress",
        assigned_to=payload.assigned_to.strip() if payload.assigned_to else user.full_name,
        notes=payload.notes.strip() if payload.notes else None,
        is_demo_sample=False,
    )
    db.add(incident)
    db.flush()

    for idx, step in enumerate(scen.steps):
        db.add(
            IncidentChecklistItem(
                incident_id=incident.id,
                phase=step.phase,
                title=step.title_bn if payload.language == "bn" else step.title_en,
                guidance=step.guidance_bn if payload.language == "bn" else step.guidance_en,
                is_completed=False,
                sort_order=idx,
            )
        )
    db.add(
        IncidentNote(
            incident_id=incident.id,
            author_name=user.full_name,
            event_type="incident_opened",
            content=f"Opened incident playbook '{incident.title}' assigned to {incident.assigned_to}.",
        )
    )

    db.commit()
    db.refresh(incident)

    record_audit_log(
        db=db,
        action="incident.opened",
        resource_type="incident",
        resource_id=str(incident.id),
        summary=f"Opened incident response playbook '{incident.title}' ({incident.severity}).",
        user_id=user.id,
        business_id=business.id,
        request=request,
    )
    return _serialize_incident(incident)


@router.get("/{incident_id}", response_model=IncidentOut)
def get_incident(incident_id: int, ctx=Depends(get_current_business), db: Session = Depends(get_db)):
    _, business = ctx
    inc = (
        db.query(Incident)
        .filter(Incident.id == incident_id, Incident.business_id == business.id)
        .first()
    )
    if not inc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found.")
    return _serialize_incident(inc)


@router.patch("/{incident_id}/items/{item_id}", response_model=IncidentOut)
def toggle_checklist_item(
    incident_id: int,
    item_id: int,
    payload: ChecklistToggleRequest,
    request: Request,
    ctx=Depends(get_current_business),
    db: Session = Depends(get_db),
):
    user, business = ctx
    inc = (
        db.query(Incident)
        .filter(Incident.id == incident_id, Incident.business_id == business.id)
        .first()
    )
    if not inc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found.")

    item = (
        db.query(IncidentChecklistItem)
        .filter(IncidentChecklistItem.id == item_id, IncidentChecklistItem.incident_id == inc.id)
        .first()
    )
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Checklist item not found.")

    item.is_completed = payload.is_completed
    item.completed_at = datetime.now(timezone.utc) if payload.is_completed else None
    db.flush()

    all_done = all(i.is_completed for i in inc.checklist_items)
    inc.status = "resolved" if all_done else "in_progress"
    inc.updated_at = datetime.now(timezone.utc)
    db.add(
        IncidentNote(
            incident_id=inc.id,
            author_name=user.full_name,
            event_type="checklist_step",
            content=f"Step '{item.title[:80]}' marked {'completed' if payload.is_completed else 'reopened'}.",
        )
    )

    db.commit()
    db.refresh(inc)

    record_audit_log(
        db=db,
        action="incident.checklist_updated",
        resource_type="incident",
        resource_id=str(inc.id),
        summary=f"Marked step '{item.title[:60]}' as {'completed' if payload.is_completed else 'open'}.",
        user_id=user.id,
        business_id=business.id,
        request=request,
    )
    return _serialize_incident(inc)


@router.patch("/{incident_id}", response_model=IncidentOut)
def update_incident_details(
    incident_id: int,
    payload: IncidentUpdateRequest,
    request: Request,
    ctx=Depends(get_current_business),
    db: Session = Depends(get_db),
):
    user, business = ctx
    inc = (
        db.query(Incident)
        .filter(Incident.id == incident_id, Incident.business_id == business.id)
        .first()
    )
    if not inc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found.")

    changes: List[str] = []
    if payload.status is not None and payload.status != inc.status:
        inc.status = payload.status
        changes.append(f"status -> {payload.status}")
    if payload.severity is not None and payload.severity != inc.severity:
        inc.severity = payload.severity
        changes.append(f"severity -> {payload.severity}")
    if payload.assigned_to is not None:
        cleaned_assignee = payload.assigned_to.strip() or None
        if cleaned_assignee != inc.assigned_to:
            inc.assigned_to = cleaned_assignee
            changes.append(f"assigned to {cleaned_assignee or 'Unassigned'}")
    if payload.resolution_summary is not None:
        inc.resolution_summary = payload.resolution_summary.strip() or None
        changes.append("updated resolution summary")

    if changes:
        inc.updated_at = datetime.now(timezone.utc)
        db.add(
            IncidentNote(
                incident_id=inc.id,
                author_name=user.full_name,
                event_type="workflow_update",
                content=f"Updated incident: {', '.join(changes)}.",
            )
        )
        db.commit()
        db.refresh(inc)
        record_audit_log(
            db=db,
            action="incident.updated",
            resource_type="incident",
            resource_id=str(inc.id),
            summary=f"Updated incident #{inc.id}: {', '.join(changes)}.",
            user_id=user.id,
            business_id=business.id,
            request=request,
        )
    return _serialize_incident(inc)


@router.post("/{incident_id}/notes", response_model=IncidentOut, status_code=status.HTTP_201_CREATED)
def add_incident_evidence_note(
    incident_id: int,
    payload: IncidentNoteCreateRequest,
    request: Request,
    ctx=Depends(get_current_business),
    db: Session = Depends(get_db),
):
    user, business = ctx
    inc = (
        db.query(Incident)
        .filter(Incident.id == incident_id, Incident.business_id == business.id)
        .first()
    )
    if not inc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found.")

    db.add(
        IncidentNote(
            incident_id=inc.id,
            author_name=user.full_name,
            event_type="evidence_note",
            content=payload.content.strip(),
        )
    )
    inc.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(inc)

    record_audit_log(
        db=db,
        action="incident.note_added",
        resource_type="incident",
        resource_id=str(inc.id),
        summary=f"Added evidence note to incident #{inc.id}.",
        user_id=user.id,
        business_id=business.id,
        request=request,
    )
    return _serialize_incident(inc)


@router.get("/{incident_id}/report.pdf")
def download_incident_report(
    incident_id: int,
    ctx=Depends(get_current_business),
    db: Session = Depends(get_db),
):
    _, business = ctx
    inc = (
        db.query(Incident)
        .filter(Incident.id == incident_id, Incident.business_id == business.id)
        .first()
    )
    if not inc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found.")
    pdf_bytes = generate_incident_pdf(inc, business.name)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="safepulse-incident-{inc.id}.pdf"'},
    )

