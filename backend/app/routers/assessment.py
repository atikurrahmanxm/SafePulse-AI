"""Business Security Health Check API routes."""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi.responses import Response
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import AssessmentAnswer, SecurityAssessment
from ..schemas import AssessmentSubmitRequest, SecurityAssessmentOut
from ..security import enforce_rate_limit, get_current_business, record_audit_log
from ..services.assessment_engine import evaluate_assessment, get_questionnaire
from ..services.pdf_report import generate_assessment_pdf


router = APIRouter(prefix="/api/assessments", tags=["Business Security Assessment"])


def _serialize_assessment(record: SecurityAssessment) -> SecurityAssessmentOut:
    answer_map = {a.question_key: a.answer_value for a in (record.answers or [])}
    return SecurityAssessmentOut(
        id=record.id,
        overall_score=record.overall_score,
        security_category=record.security_category,
        category_scores=record.category_scores,
        weak_areas=record.weak_areas,
        critical_gaps=record.critical_gaps,
        recommendations=record.recommendations,
        answers=answer_map,
        is_demo_sample=record.is_demo_sample,
        created_at=record.created_at,
        updated_at=record.updated_at,
    )


@router.get("/questions")
def get_questions(language: str = Query("en", pattern="^(en|bn)$")):
    return {"questions": get_questionnaire(language)}


@router.post("/submit", response_model=SecurityAssessmentOut, status_code=status.HTTP_201_CREATED)
def submit_assessment(
    payload: AssessmentSubmitRequest,
    request: Request,
    ctx=Depends(get_current_business),
    db: Session = Depends(get_db),
):
    enforce_rate_limit(request, bucket_suffix="assessment_submit", limit=30)
    user, business = ctx

    try:
        result = evaluate_assessment(payload.answers, language=payload.language)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc

    record = SecurityAssessment(
        business_id=business.id,
        user_id=user.id,
        overall_score=result["overall_score"],
        security_category=result["security_category"],
        category_scores=result["category_scores"],
        weak_areas=result["weak_areas"],
        critical_gaps=result["critical_gaps"],
        recommendations=result["recommendations"],
        is_demo_sample=False,
    )
    db.add(record)
    db.flush()

    for row in result["answer_rows"]:
        db.add(AssessmentAnswer(assessment_id=record.id, **row))

    db.commit()
    db.refresh(record)

    record_audit_log(
        db=db,
        action="assessment.completed",
        resource_type="security_assessment",
        resource_id=str(record.id),
        summary=f"Completed Business Security Assessment — Score {record.overall_score}/100 ({record.security_category}).",
        user_id=user.id,
        business_id=business.id,
        request=request,
    )
    return _serialize_assessment(record)


@router.get("/latest")
def get_latest_assessment(ctx=Depends(get_current_business), db: Session = Depends(get_db)):
    _, business = ctx
    record = (
        db.query(SecurityAssessment)
        .filter(SecurityAssessment.business_id == business.id)
        .order_by(SecurityAssessment.created_at.desc())
        .first()
    )
    if not record:
        return {"assessment": None}
    return {"assessment": _serialize_assessment(record)}


@router.get("/history", response_model=List[SecurityAssessmentOut])
def list_assessment_history(ctx=Depends(get_current_business), db: Session = Depends(get_db)):
    _, business = ctx
    records = (
        db.query(SecurityAssessment)
        .filter(SecurityAssessment.business_id == business.id)
        .order_by(SecurityAssessment.created_at.desc())
        .limit(20)
        .all()
    )
    return [_serialize_assessment(r) for r in records]


@router.get("/{assessment_id}/report.pdf")
def download_assessment_report(
    assessment_id: int,
    ctx=Depends(get_current_business),
    db: Session = Depends(get_db),
):
    _, business = ctx
    record = (
        db.query(SecurityAssessment)
        .filter(SecurityAssessment.id == assessment_id, SecurityAssessment.business_id == business.id)
        .first()
    )
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Security assessment not found.")
    pdf_bytes = generate_assessment_pdf(record, business.name)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="cybershield-assessment-{record.id}.pdf"'},
    )

