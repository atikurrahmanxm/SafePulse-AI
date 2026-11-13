"""Data Breach & Exposure Monitoring Router for SafePulse AI."""

from __future__ import annotations

from typing import Any, Dict, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Business, User
from ..security import get_current_business
from ..services.breach_engine import check_breach_exposure
from ..services.pdf_report import _build_pdf

router = APIRouter(prefix="/api/breaches", tags=["Data Breach Monitoring"])


class BreachCheckRequest(BaseModel):
    query: str = Field(..., min_length=3, max_length=150, description="Email or domain to inspect for breach exposure")
    language: str = Field("en", pattern="^(en|bn)$")


@router.post("/check", response_model=Dict[str, Any])
def check_exposure_endpoint(
    req: BreachCheckRequest,
    ctx=Depends(get_current_business),
):
    user, business = ctx
    try:
        result = check_breach_exposure(req.query, req.language)
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))


@router.get("/demo-sample", response_model=Dict[str, Any])
def get_demo_breach_sample(language: str = Query("en", pattern="^(en|bn)$")):
    """Returns a realistic simulated breach exposure check for live hackathon demonstration."""
    return check_breach_exposure("owner@brahmaputra-care.in", language=language)


@router.get("/report.pdf")
def download_breach_pdf(
    query: str = Query(..., min_length=3),
    language: str = Query("en", pattern="^(en|bn)$"),
    ctx=Depends(get_current_business),
):
    """Generates a downloadable PDF summary for a data breach exposure check."""
    user, business = ctx
    try:
        data = check_breach_exposure(query, language=language)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))

    summary_table = [
        ["Target Identifier", data["query"]],
        ["Identifier Type", data["query_type"].upper()],
        ["Identified Breaches", f"{data['exposure_count']} Incident(s)"],
        ["Exposure Risk Level", f"{data['risk_level']} ({data['risk_score']} / 100)"],
        ["Exposed Data Classes", ", ".join(data["data_classes_exposed"]) or "None Detected"],
        ["Status Verdict", data["category"]],
    ]

    sections = [
        {"heading": "Executive Assessment", "text": data["summary"]},
        {
            "heading": "Matched Breach Incidents",
            "items": [
                f"{b['title']} ({b['breach_date']}): {b['description']} [Exposed: {', '.join(b['data_classes'])}]"
                for b in data["breaches"]
            ]
            or ["No public breach incidents matched this identifier."],
        },
        {
            "heading": "Recommended Incident Remediation Actions",
            "items": data["recommended_actions"],
        },
    ]

    limitation = (
        "SafePulse AI Data Breach Monitoring checks offline threat repositories and simulated benchmark databases. "
        "It provides actionable early-warning triage for small business owners and does not store or share plaintext passwords."
    )

    pdf_bytes = _build_pdf(
        f"Data Breach Exposure Report ({data['query']})",
        business.name,
        data["checked_at"],
        summary_table,
        sections,
        limitation,
    )

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="safepulse-breach-report-{data["query"][:20]}.pdf"'},
    )
