"""Authentication, demo session, and business profile routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Business, User
from ..schemas import (
    AuthResponse,
    BusinessCreateRequest,
    BusinessProfileOut,
    BusinessUpdateRequest,
    UserLoginRequest,
    UserOut,
    UserRegisterRequest,
)
from ..security import (
    create_access_token,
    enforce_rate_limit,
    get_current_business,
    get_current_user,
    hash_password,
    record_audit_log,
    verify_password,
)
from ..services.demo_seeder import ensure_demo_workspace, ensure_quizzes_seeded
from ..services.governance_engine import SUBSCRIPTION_PLANS


router = APIRouter(prefix="/api/auth", tags=["Authentication"])


def _to_business_out(business: Business) -> BusinessProfileOut:
    return BusinessProfileOut(
        id=business.id,
        name=business.name,
        industry=business.industry,
        employee_count=business.employee_count,
        city=business.city,
        primary_email_domain=business.primary_email_domain,
        is_demo_workspace=business.is_demo_workspace,
        subscription_tier=business.subscription_tier,
        monthly_scan_quota=business.monthly_scan_quota,
    )


def _to_user_out(user: User, business: Business, db: Session | None = None) -> UserOut:
    all_businesses = (
        db.query(Business).filter(Business.owner_id == user.id).order_by(Business.id.asc()).all()
        if db is not None
        else [business]
    )
    return UserOut(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        role=user.role,
        preferred_language=user.preferred_language,
        is_demo=user.is_demo,
        business=_to_business_out(business),
        businesses=[_to_business_out(b) for b in all_businesses],
    )


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def register(payload: UserRegisterRequest, request: Request, db: Session = Depends(get_db)):
    enforce_rate_limit(request, bucket_suffix="auth_register", limit=20)
    ensure_quizzes_seeded(db)

    normalized_email = payload.email.lower().strip()
    existing = db.query(User).filter(User.email == normalized_email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists.",
        )

    user = User(
        email=normalized_email,
        full_name=payload.full_name.strip(),
        password_hash=hash_password(payload.password),
        role="owner",
        preferred_language="en",
        is_demo=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    business = Business(
        owner_id=user.id,
        name=payload.business_name.strip(),
        industry=payload.industry.strip(),
        employee_count=payload.employee_count,
        city=payload.city.strip(),
        is_demo_workspace=False,
    )
    db.add(business)
    db.commit()
    db.refresh(business)

    record_audit_log(
        db=db,
        action="user.registered",
        resource_type="user",
        resource_id=str(user.id),
        summary=f"Registered account and business workspace '{business.name}'.",
        user_id=user.id,
        business_id=business.id,
        request=request,
    )

    token = create_access_token(user.id, user.email, is_demo=False)
    return AuthResponse(access_token=token, user=_to_user_out(user, business, db))


@router.post("/login", response_model=AuthResponse)
def login(payload: UserLoginRequest, request: Request, db: Session = Depends(get_db)):
    enforce_rate_limit(request, bucket_suffix="auth_login", limit=30)
    normalized_email = payload.email.lower().strip()
    user = db.query(User).filter(User.email == normalized_email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    business = db.query(Business).filter(Business.owner_id == user.id).order_by(Business.id.asc()).first()
    if not business:
        business = Business(owner_id=user.id, name=f"{user.full_name}'s Business", is_demo_workspace=user.is_demo)
        db.add(business)
        db.commit()
        db.refresh(business)

    record_audit_log(
        db=db,
        action="user.logged_in",
        resource_type="user",
        resource_id=str(user.id),
        summary="Authenticated session started.",
        user_id=user.id,
        business_id=business.id,
        request=request,
    )

    token = create_access_token(user.id, user.email, is_demo=user.is_demo)
    return AuthResponse(access_token=token, user=_to_user_out(user, business, db))


@router.post("/demo", response_model=AuthResponse)
def demo_login(request: Request, db: Session = Depends(get_db)):
    enforce_rate_limit(request, bucket_suffix="auth_demo", limit=30)
    demo_user = ensure_demo_workspace(db)
    business = db.query(Business).filter(Business.owner_id == demo_user.id).first()
    token = create_access_token(demo_user.id, demo_user.email, is_demo=True)
    record_audit_log(
        db=db,
        action="demo.session_started",
        resource_type="user",
        resource_id=str(demo_user.id),
        summary="Started Hackathon Demo Mode session.",
        user_id=demo_user.id,
        business_id=business.id,
        request=request,
    )
    return AuthResponse(access_token=token, user=_to_user_out(demo_user, business, db))


@router.post("/logout")
def logout(request: Request, ctx=Depends(get_current_business), db: Session = Depends(get_db)):
    user, business = ctx
    record_audit_log(
        db=db,
        action="user.logged_out",
        resource_type="user",
        resource_id=str(user.id),
        summary="User signed out of CyberShield AI.",
        user_id=user.id,
        business_id=business.id,
        request=request,
    )
    return {"status": "ok", "message": "Signed out successfully."}


@router.get("/me", response_model=UserOut)
def get_me(ctx=Depends(get_current_business), db: Session = Depends(get_db)):
    user, business = ctx
    return _to_user_out(user, business, db)


@router.post("/businesses", response_model=BusinessProfileOut, status_code=status.HTTP_201_CREATED)
def create_workspace(
    payload: BusinessCreateRequest,
    request: Request,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    enforce_rate_limit(request, bucket_suffix="biz_create", limit=20)
    existing_count = db.query(Business).filter(Business.owner_id == user.id).count()
    first_biz = db.query(Business).filter(Business.owner_id == user.id).order_by(Business.id.asc()).first()
    tier = first_biz.subscription_tier if first_biz else "free"
    plan = SUBSCRIPTION_PLANS.get(tier, SUBSCRIPTION_PLANS["free"])
    if existing_count >= plan["max_workspaces"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Workspace limit ({plan['max_workspaces']}) reached for {plan['name']}.",
        )
    biz = Business(
        owner_id=user.id,
        name=payload.name.strip(),
        industry=payload.industry.strip(),
        employee_count=payload.employee_count,
        city=payload.city.strip(),
        primary_email_domain=payload.primary_email_domain.strip() if payload.primary_email_domain else None,
        is_demo_workspace=user.is_demo,
        subscription_tier=tier,
        monthly_scan_quota=plan["monthly_scan_quota"],
    )
    db.add(biz)
    db.commit()
    db.refresh(biz)
    record_audit_log(
        db=db,
        action="business.created",
        resource_type="business",
        resource_id=str(biz.id),
        summary=f"Created additional business workspace '{biz.name}'.",
        user_id=user.id,
        business_id=biz.id,
        request=request,
    )
    return _to_business_out(biz)


@router.put("/business", response_model=UserOut)
def update_business(
    payload: BusinessUpdateRequest,
    request: Request,
    ctx=Depends(get_current_business),
    db: Session = Depends(get_db),
):
    user, business = ctx
    business.name = payload.name.strip()
    business.industry = payload.industry.strip()
    business.employee_count = payload.employee_count
    business.city = payload.city.strip()
    business.primary_email_domain = payload.primary_email_domain.strip() if payload.primary_email_domain else None
    user.preferred_language = payload.preferred_language
    if payload.subscription_tier and payload.subscription_tier in SUBSCRIPTION_PLANS:
        business.subscription_tier = payload.subscription_tier
        business.monthly_scan_quota = SUBSCRIPTION_PLANS[payload.subscription_tier]["monthly_scan_quota"]
    db.commit()
    db.refresh(user)
    db.refresh(business)

    record_audit_log(
        db=db,
        action="business.updated",
        resource_type="business",
        resource_id=str(business.id),
        summary=f"Updated business profile '{business.name}' (tier={business.subscription_tier}).",
        user_id=user.id,
        business_id=business.id,
        request=request,
    )
    return _to_user_out(user, business, db)

