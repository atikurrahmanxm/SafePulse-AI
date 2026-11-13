"""SSRF-safe Smart URL Security Scanner API routes."""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import Response
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import URLScan
from ..schemas import URLScanOut, URLScanRequest
from ..security import enforce_rate_limit, get_current_business, record_audit_log
from ..services.demo_seeder import HACKATHON_SAMPLE_URLS
from ..services.pdf_report import generate_url_pdf
from ..services.url_analyzer import SSRFBlockedError, analyze_url


router = APIRouter(prefix="/api/urls", tags=["URL Security Scanner"])


@router.get("/samples")
def get_url_samples():
    return {"samples": HACKATHON_SAMPLE_URLS}


@router.post("/scan", response_model=URLScanOut, status_code=status.HTTP_201_CREATED)
def scan_url(
    payload: URLScanRequest,
    request: Request,
    ctx=Depends(get_current_business),
    db: Session = Depends(get_db),
):
    enforce_rate_limit(request, bucket_suffix="url_scan", limit=45)
    user, business = ctx

    try:
        result = analyze_url(payload.url, language=payload.language)
    except SSRFBlockedError as exc:
        record_audit_log(
            db=db,
            action="url.ssrf_blocked",
            resource_type="url_scan",
            summary=f"Blocked unsafe/internal URL submission: {payload.url[:100]}",
            user_id=user.id,
            business_id=business.id,
            request=request,
        )
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc

    record = URLScan(
        business_id=business.id,
        user_id=user.id,
        submitted_url=result["submitted_url"],
        normalized_host=result["normalized_host"],
        scheme=result["scheme"],
        risk_score=result["risk_score"],
        risk_category=result["risk_category"],
        verdict_classification=result["verdict_classification"],
        indicators=result["indicators"],
        dns_records=result["dns_records"],
        tls_info=result["tls_info"],
        reputation_source=result["reputation_source"],
        technical_explanation=result["technical_explanation"],
        recommendations=result["recommendations"],
        is_demo_sample=False,
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    record_audit_log(
        db=db,
        action="url.scanned",
        resource_type="url_scan",
        resource_id=str(record.id),
        summary=f"Scanned URL '{record.normalized_host}' — Score {record.risk_score}/100 ({record.risk_category}).",
        user_id=user.id,
        business_id=business.id,
        request=request,
    )
    return record


@router.get("/history", response_model=List[URLScanOut])
def list_url_history(ctx=Depends(get_current_business), db: Session = Depends(get_db)):
    _, business = ctx
    return (
        db.query(URLScan)
        .filter(URLScan.business_id == business.id)
        .order_by(URLScan.created_at.desc())
        .limit(50)
        .all()
    )


@router.get("/{scan_id}", response_model=URLScanOut)
def get_url_scan(
    scan_id: int,
    ctx=Depends(get_current_business),
    db: Session = Depends(get_db),
):
    _, business = ctx
    record = (
        db.query(URLScan)
        .filter(URLScan.id == scan_id, URLScan.business_id == business.id)
        .first()
    )
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL scan record not found.")
    return record


@router.get("/{scan_id}/report.pdf")
def download_url_report(
    scan_id: int,
    ctx=Depends(get_current_business),
    db: Session = Depends(get_db),
):
    _, business = ctx
    record = (
        db.query(URLScan)
        .filter(URLScan.id == scan_id, URLScan.business_id == business.id)
        .first()
    )
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL scan record not found.")
    pdf_bytes = generate_url_pdf(record, business.name)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="safepulse-url-{record.id}.pdf"'},
    )

