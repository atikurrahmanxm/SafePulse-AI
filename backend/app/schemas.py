"""Pydantic v2 request and response schemas with strict validation."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    full_name: str = Field(min_length=2, max_length=120)
    business_name: str = Field(min_length=2, max_length=160)
    industry: str = Field(default="Retail & Local Shop", min_length=2, max_length=80)
    employee_count: int = Field(default=8, ge=1, le=5000)
    city: str = Field(default="Guwahati", min_length=2, max_length=80)

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, value: str) -> str:
        if not any(ch.isalpha() for ch in value) or not any(ch.isdigit() for ch in value):
            raise ValueError("Password must include at least one letter and one digit.")
        return value


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class BusinessProfileOut(BaseModel):
    id: int
    name: str
    industry: str
    employee_count: int
    city: str
    primary_email_domain: Optional[str] = None
    is_demo_workspace: bool
    subscription_tier: str = "free"
    monthly_scan_quota: int = 50


class BusinessCreateRequest(BaseModel):
    name: str = Field(min_length=2, max_length=160)
    industry: str = Field(default="Retail & Local Shop", min_length=2, max_length=80)
    employee_count: int = Field(default=8, ge=1, le=5000)
    city: str = Field(default="Guwahati", min_length=2, max_length=80)
    primary_email_domain: Optional[str] = Field(default=None, max_length=120)


class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: str
    preferred_language: str
    is_demo: bool
    business: BusinessProfileOut
    businesses: List[BusinessProfileOut] = Field(default_factory=list)


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class BusinessUpdateRequest(BaseModel):
    name: str = Field(min_length=2, max_length=160)
    industry: str = Field(min_length=2, max_length=80)
    employee_count: int = Field(ge=1, le=5000)
    city: str = Field(min_length=2, max_length=80)
    primary_email_domain: Optional[str] = Field(default=None, max_length=120)
    preferred_language: Literal["en", "bn"] = "en"
    subscription_tier: Optional[Literal["free", "pro_sme", "enterprise_ready"]] = None


class PhishingAnalyzeRequest(BaseModel):
    message: str = Field(min_length=10, max_length=10000)
    channel: Literal["email", "sms", "whatsapp", "other"] = "email"
    sender_hint: Optional[str] = Field(default=None, max_length=255)
    language: Literal["en", "bn"] = "en"

    @field_validator("message")
    @classmethod
    def strip_and_check(cls, value: str) -> str:
        cleaned = value.strip()
        if len(cleaned) < 10:
            raise ValueError("Message must contain at least 10 non-whitespace characters.")
        return cleaned


class HighlightedPhraseOut(BaseModel):
    phrase: str
    category: str
    weight: int
    start: int
    end: int


class PhishingAnalysisOut(BaseModel):
    id: int
    channel: str
    sender_hint: Optional[str] = None
    message_excerpt: str
    raw_message: str
    risk_score: int
    risk_category: str
    ml_probability: float
    model_confidence: float
    highlighted_phrases: List[HighlightedPhraseOut]
    social_engineering_tactics: List[Dict[str, Any]] = Field(default_factory=list)
    reasons: List[str]
    recommendations: List[str]
    is_demo_sample: bool
    created_at: datetime


class URLScanRequest(BaseModel):
    url: str = Field(min_length=4, max_length=1024)
    language: Literal["en", "bn"] = "en"

    @field_validator("url")
    @classmethod
    def strip_url(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned or any(ch.isspace() for ch in cleaned):
            raise ValueError("URL cannot be empty or contain spaces.")
        return cleaned


class URLIndicatorOut(BaseModel):
    code: str
    label: str
    severity: Literal["info", "low", "medium", "high", "critical"]
    detail: str
    score_impact: int


class URLScanOut(BaseModel):
    id: int
    submitted_url: str
    normalized_host: str
    scheme: str
    risk_score: int
    risk_category: str
    verdict_classification: str = "Unknown"
    indicators: List[URLIndicatorOut]
    dns_records: Dict[str, Any]
    tls_info: Dict[str, Any] = Field(default_factory=dict)
    reputation_source: str
    technical_explanation: str
    recommendations: List[str]
    is_demo_sample: bool
    created_at: datetime


class AssessmentSubmitRequest(BaseModel):
    answers: Dict[str, str] = Field(min_length=1)
    language: Literal["en", "bn"] = "en"


class SecurityAssessmentOut(BaseModel):
    id: int
    overall_score: int
    security_category: str
    category_scores: Dict[str, int]
    weak_areas: List[str]
    critical_gaps: List[str]
    recommendations: List[Dict[str, Any]]
    answers: Dict[str, str]
    is_demo_sample: bool
    created_at: datetime
    updated_at: datetime


class IncidentCreateRequest(BaseModel):
    scenario_key: str = Field(min_length=2, max_length=64)
    title: Optional[str] = Field(default=None, max_length=180)
    assigned_to: Optional[str] = Field(default=None, max_length=120)
    notes: Optional[str] = Field(default=None, max_length=2000)
    language: Literal["en", "bn"] = "en"


class IncidentUpdateRequest(BaseModel):
    status: Optional[Literal["in_progress", "contained", "resolved"]] = None
    severity: Optional[Literal["Low", "Medium", "High", "Critical"]] = None
    assigned_to: Optional[str] = Field(default=None, max_length=120)
    resolution_summary: Optional[str] = Field(default=None, max_length=2000)


class IncidentNoteCreateRequest(BaseModel):
    content: str = Field(min_length=3, max_length=2000)


class IncidentNoteOut(BaseModel):
    id: int
    author_name: str
    event_type: str
    content: str
    created_at: datetime


class ChecklistToggleRequest(BaseModel):
    is_completed: bool


class IncidentChecklistItemOut(BaseModel):
    id: int
    phase: str
    title: str
    guidance: str
    is_completed: bool
    completed_at: Optional[datetime] = None
    sort_order: int


class IncidentOut(BaseModel):
    id: int
    scenario_key: str
    title: str
    severity: str
    status: str
    assigned_to: Optional[str] = None
    resolution_summary: Optional[str] = None
    notes: Optional[str] = None
    progress_percent: int
    completed_count: int
    total_count: int
    is_demo_sample: bool
    created_at: datetime
    updated_at: datetime
    checklist_items: List[IncidentChecklistItemOut]
    timeline_notes: List[IncidentNoteOut] = Field(default_factory=list)


class BusinessMemberCreateRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    role: Literal["owner", "manager", "staff"] = "staff"
    department: str = Field(default="Operations", min_length=2, max_length=80)
    mfa_enabled: bool = False
    awareness_trained: bool = False


class BusinessMemberUpdateRequest(BaseModel):
    role: Optional[Literal["owner", "manager", "staff"]] = None
    department: Optional[str] = Field(default=None, min_length=2, max_length=80)
    mfa_enabled: Optional[bool] = None
    awareness_trained: Optional[bool] = None


class BusinessMemberOut(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    role: str
    department: str
    mfa_enabled: bool
    awareness_trained: bool
    created_at: datetime


class BusinessControlUpdateRequest(BaseModel):
    is_completed: Optional[bool] = None
    owner_name: Optional[str] = Field(default=None, max_length=120)
    target_date: Optional[str] = Field(default=None, max_length=32)


class BusinessControlOut(BaseModel):
    id: int
    category: str
    control_key: str
    title: str
    guidance: str
    priority: str
    is_completed: bool
    owner_name: Optional[str] = None
    target_date: Optional[str] = None
    last_verified_at: Optional[datetime] = None


class IntegrationUpdateRequest(BaseModel):
    enabled: bool
    endpoint_or_account: Optional[str] = Field(default=None, max_length=255)
    notes: Optional[str] = Field(default=None, max_length=255)


class QuizSubmitRequest(BaseModel):
    answers: Dict[str, int]


class QuizResultOut(BaseModel):
    id: int
    quiz_slug: str
    quiz_title: str
    score: int
    total_questions: int
    percentage: float
    answers_summary: List[Dict[str, Any]]
    created_at: datetime

