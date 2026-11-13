"""Relational database models for CyberShield AI (SQLite & PostgreSQL compatible)."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    JSON,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    full_name: Mapped[str] = mapped_column(String(120), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(32), default="owner", nullable=False)
    preferred_language: Mapped[str] = mapped_column(String(8), default="en", nullable=False)
    is_demo: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False
    )

    businesses: Mapped[List["Business"]] = relationship(
        back_populates="owner", cascade="all, delete-orphan"
    )
    quiz_results: Mapped[List["QuizResult"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


class Business(Base):
    __tablename__ = "businesses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    owner_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    industry: Mapped[str] = mapped_column(String(80), default="Retail & Local Shop", nullable=False)
    employee_count: Mapped[int] = mapped_column(Integer, default=10, nullable=False)
    city: Mapped[str] = mapped_column(String(80), default="Guwahati", nullable=False)
    primary_email_domain: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    is_demo_workspace: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    subscription_tier: Mapped[str] = mapped_column(String(32), default="free", nullable=False)
    monthly_scan_quota: Mapped[int] = mapped_column(Integer, default=50, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False
    )

    owner: Mapped["User"] = relationship(back_populates="businesses")
    phishing_analyses: Mapped[List["PhishingAnalysis"]] = relationship(
        back_populates="business", cascade="all, delete-orphan"
    )
    url_scans: Mapped[List["URLScan"]] = relationship(
        back_populates="business", cascade="all, delete-orphan"
    )
    assessments: Mapped[List["SecurityAssessment"]] = relationship(
        back_populates="business", cascade="all, delete-orphan"
    )
    incidents: Mapped[List["Incident"]] = relationship(
        back_populates="business", cascade="all, delete-orphan"
    )
    members: Mapped[List["BusinessMember"]] = relationship(
        back_populates="business", cascade="all, delete-orphan"
    )
    controls: Mapped[List["BusinessControl"]] = relationship(
        back_populates="business", cascade="all, delete-orphan"
    )
    integrations: Mapped[List["IntegrationConfig"]] = relationship(
        back_populates="business", cascade="all, delete-orphan"
    )


class PhishingAnalysis(Base):
    __tablename__ = "phishing_analyses"
    __table_args__ = (
        Index("ix_phishing_business_created", "business_id", "created_at"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    business_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False, index=True
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    channel: Mapped[str] = mapped_column(String(32), default="email", nullable=False)
    sender_hint: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    message_excerpt: Mapped[str] = mapped_column(String(240), nullable=False)
    raw_message: Mapped[str] = mapped_column(Text, nullable=False)
    risk_score: Mapped[int] = mapped_column(Integer, nullable=False)
    risk_category: Mapped[str] = mapped_column(String(32), nullable=False)
    ml_probability: Mapped[float] = mapped_column(Float, nullable=False)
    model_confidence: Mapped[float] = mapped_column(Float, nullable=False)
    highlighted_phrases: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    social_engineering_tactics: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    reasons: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    recommendations: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    is_demo_sample: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

    business: Mapped["Business"] = relationship(back_populates="phishing_analyses")


class URLScan(Base):
    __tablename__ = "url_scans"
    __table_args__ = (
        Index("ix_url_business_created", "business_id", "created_at"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    business_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False, index=True
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    submitted_url: Mapped[str] = mapped_column(String(1024), nullable=False)
    normalized_host: Mapped[str] = mapped_column(String(255), nullable=False)
    scheme: Mapped[str] = mapped_column(String(16), nullable=False)
    risk_score: Mapped[int] = mapped_column(Integer, nullable=False)
    risk_category: Mapped[str] = mapped_column(String(32), nullable=False)
    verdict_classification: Mapped[str] = mapped_column(String(48), default="Unknown", nullable=False)
    indicators: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    dns_records: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    tls_info: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    reputation_source: Mapped[str] = mapped_column(String(64), default="local-engine", nullable=False)
    technical_explanation: Mapped[str] = mapped_column(Text, nullable=False)
    recommendations: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    is_demo_sample: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

    business: Mapped["Business"] = relationship(back_populates="url_scans")


class SecurityAssessment(Base):
    __tablename__ = "security_assessments"
    __table_args__ = (
        Index("ix_assessment_business_created", "business_id", "created_at"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    business_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False, index=True
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    overall_score: Mapped[int] = mapped_column(Integer, nullable=False)
    security_category: Mapped[str] = mapped_column(String(32), nullable=False)
    category_scores: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    weak_areas: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    critical_gaps: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    recommendations: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    is_demo_sample: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False
    )

    business: Mapped["Business"] = relationship(back_populates="assessments")
    answers: Mapped[List["AssessmentAnswer"]] = relationship(
        back_populates="assessment", cascade="all, delete-orphan"
    )


class AssessmentAnswer(Base):
    __tablename__ = "assessment_answers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    assessment_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("security_assessments.id", ondelete="CASCADE"), nullable=False, index=True
    )
    question_key: Mapped[str] = mapped_column(String(64), nullable=False)
    domain: Mapped[str] = mapped_column(String(64), nullable=False)
    answer_value: Mapped[str] = mapped_column(String(32), nullable=False)
    score_awarded: Mapped[int] = mapped_column(Integer, nullable=False)
    max_score: Mapped[int] = mapped_column(Integer, nullable=False)

    assessment: Mapped["SecurityAssessment"] = relationship(back_populates="answers")


class Incident(Base):
    __tablename__ = "incidents"
    __table_args__ = (
        Index("ix_incident_business_created", "business_id", "created_at"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    business_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False, index=True
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    scenario_key: Mapped[str] = mapped_column(String(64), nullable=False)
    title: Mapped[str] = mapped_column(String(180), nullable=False)
    severity: Mapped[str] = mapped_column(String(24), nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="in_progress", nullable=False)
    assigned_to: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    resolution_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_demo_sample: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False
    )

    business: Mapped["Business"] = relationship(back_populates="incidents")
    checklist_items: Mapped[List["IncidentChecklistItem"]] = relationship(
        back_populates="incident", cascade="all, delete-orphan", order_by="IncidentChecklistItem.sort_order"
    )
    timeline_notes: Mapped[List["IncidentNote"]] = relationship(
        back_populates="incident", cascade="all, delete-orphan", order_by="IncidentNote.created_at"
    )


class IncidentChecklistItem(Base):
    __tablename__ = "incident_checklist_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    incident_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("incidents.id", ondelete="CASCADE"), nullable=False, index=True
    )
    phase: Mapped[str] = mapped_column(String(48), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    guidance: Mapped[str] = mapped_column(Text, nullable=False)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    incident: Mapped["Incident"] = relationship(back_populates="checklist_items")


class AwarenessQuiz(Base):
    __tablename__ = "awareness_quizzes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    slug: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(160), nullable=False)
    topic: Mapped[str] = mapped_column(String(64), nullable=False)
    difficulty: Mapped[str] = mapped_column(String(32), default="Beginner", nullable=False)
    questions_count: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

    results: Mapped[List["QuizResult"]] = relationship(
        back_populates="quiz", cascade="all, delete-orphan"
    )


class QuizResult(Base):
    __tablename__ = "quiz_results"
    __table_args__ = (
        Index("ix_quiz_result_user_created", "user_id", "created_at"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    quiz_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("awareness_quizzes.id", ondelete="CASCADE"), nullable=False, index=True
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    business_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False, index=True
    )
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    total_questions: Mapped[int] = mapped_column(Integer, nullable=False)
    percentage: Mapped[float] = mapped_column(Float, nullable=False)
    answers_summary: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

    quiz: Mapped["AwarenessQuiz"] = relationship(back_populates="results")
    user: Mapped["User"] = relationship(back_populates="quiz_results")


class AuditLog(Base):
    __tablename__ = "audit_logs"
    __table_args__ = (
        Index("ix_audit_business_created", "business_id", "created_at"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )
    business_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("businesses.id", ondelete="SET NULL"), nullable=True, index=True
    )
    action: Mapped[str] = mapped_column(String(80), nullable=False)
    resource_type: Mapped[str] = mapped_column(String(48), nullable=False)
    resource_id: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    summary: Mapped[str] = mapped_column(String(255), nullable=False)
    ip_address: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)


class IncidentNote(Base):
    __tablename__ = "incident_notes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    incident_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("incidents.id", ondelete="CASCADE"), nullable=False, index=True
    )
    author_name: Mapped[str] = mapped_column(String(120), nullable=False)
    event_type: Mapped[str] = mapped_column(String(32), default="evidence_note", nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

    incident: Mapped["Incident"] = relationship(back_populates="timeline_notes")


class BusinessMember(Base):
    __tablename__ = "business_members"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    business_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False, index=True
    )
    full_name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(32), default="staff", nullable=False)
    department: Mapped[str] = mapped_column(String(80), default="Operations", nullable=False)
    mfa_enabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    awareness_trained: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False
    )

    business: Mapped["Business"] = relationship(back_populates="members")


class BusinessControl(Base):
    __tablename__ = "business_controls"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    business_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False, index=True
    )
    category: Mapped[str] = mapped_column(String(32), nullable=False)  # backup | updates | policy | roadmap
    control_key: Mapped[str] = mapped_column(String(80), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    guidance: Mapped[str] = mapped_column(Text, nullable=False)
    priority: Mapped[str] = mapped_column(String(16), default="Medium", nullable=False)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    owner_name: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    target_date: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    last_verified_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False
    )

    business: Mapped["Business"] = relationship(back_populates="controls")


class IntegrationConfig(Base):
    __tablename__ = "integration_configs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    business_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("businesses.id", ondelete="CASCADE"), nullable=False, index=True
    )
    provider_key: Mapped[str] = mapped_column(String(64), nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    endpoint_or_account: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False
    )

    business: Mapped["Business"] = relationship(back_populates="integrations")

