"""AI Phishing & Scam Detector API routes."""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import Response
from sqlalchemy.orm import Session

from ..database import get_db
from ..ml.predictor import analyze_message
from ..ml.trainer import get_model_and_metrics
from ..models import PhishingAnalysis
from ..schemas import PhishingAnalysisOut, PhishingAnalyzeRequest
from ..security import enforce_rate_limit, get_current_business, record_audit_log
from ..services.demo_seeder import HACKATHON_SAMPLE_MESSAGES
from ..services.pdf_report import generate_phishing_pdf


router = APIRouter(prefix="/api/phishing", tags=["Phishing Detector"])


@router.get("/samples")
def get_phishing_samples():
    return {"samples": HACKATHON_SAMPLE_MESSAGES}


@router.get("/model-evaluation")
def get_ml_evaluation():
    _, metrics = get_model_and_metrics()
    return metrics


@router.post("/analyze", response_model=PhishingAnalysisOut, status_code=status.HTTP_201_CREATED)
def analyze_phishing_message(
    payload: PhishingAnalyzeRequest,
    request: Request,
    ctx=Depends(get_current_business),
    db: Session = Depends(get_db),
):
    enforce_rate_limit(request, bucket_suffix="phishing_analyze", limit=45)
    user, business = ctx

    result = analyze_message(
        message=payload.message,
        channel=payload.channel,
        sender_hint=payload.sender_hint,
        language=payload.language,
    )

    record = PhishingAnalysis(
        business_id=business.id,
        user_id=user.id,
        channel=result["channel"],
        sender_hint=result["sender_hint"],
        message_excerpt=result["message_excerpt"],
        raw_message=result["raw_message"],
        risk_score=result["risk_score"],
        risk_category=result["risk_category"],
        ml_probability=result["ml_probability"],
        model_confidence=result["model_confidence"],
        highlighted_phrases=result["highlighted_phrases"],
        social_engineering_tactics=result["social_engineering_tactics"],
        reasons=result["reasons"],
        recommendations=result["recommendations"],
        is_demo_sample=False,
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    record_audit_log(
        db=db,
        action="phishing.analyzed",
        resource_type="phishing_analysis",
        resource_id=str(record.id),
        summary=f"Analyzed {record.channel} message — Score {record.risk_score}/100 ({record.risk_category}).",
        user_id=user.id,
        business_id=business.id,
        request=request,
    )
    return record


@router.get("/history", response_model=List[PhishingAnalysisOut])
def list_phishing_history(ctx=Depends(get_current_business), db: Session = Depends(get_db)):
    _, business = ctx
    return (
        db.query(PhishingAnalysis)
        .filter(PhishingAnalysis.business_id == business.id)
        .order_by(PhishingAnalysis.created_at.desc())
        .limit(50)
        .all()
    )


@router.get("/{analysis_id}", response_model=PhishingAnalysisOut)
def get_phishing_analysis(
    analysis_id: int,
    ctx=Depends(get_current_business),
    db: Session = Depends(get_db),
):
    _, business = ctx
    record = (
        db.query(PhishingAnalysis)
        .filter(PhishingAnalysis.id == analysis_id, PhishingAnalysis.business_id == business.id)
        .first()
    )
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Phishing analysis record not found.")
    return record


@router.get("/{analysis_id}/report.pdf")
def download_phishing_report(
    analysis_id: int,
    ctx=Depends(get_current_business),
    db: Session = Depends(get_db),
):
    _, business = ctx
    record = (
        db.query(PhishingAnalysis)
        .filter(PhishingAnalysis.id == analysis_id, PhishingAnalysis.business_id == business.id)
        .first()
    )
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Phishing analysis record not found.")
    pdf_bytes = generate_phishing_pdf(record, business.name)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="cybershield-phishing-{record.id}.pdf"'},
    )

