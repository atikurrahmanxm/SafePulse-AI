"""Security primitives: Argon2 password hashing, JWT tokens, rate limiting, and tenant isolation."""

from __future__ import annotations

import threading
import time
from collections import defaultdict, deque
from datetime import datetime, timedelta, timezone
from typing import Deque, Dict, Optional, Tuple

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from .config import settings
from .database import get_db
from .models import AuditLog, Business, User


password_hasher = PasswordHasher(
    time_cost=2,
    memory_cost=65536,
    parallelism=2,
)
bearer_scheme = HTTPBearer(auto_error=False)


def hash_password(password: str) -> str:
    return password_hasher.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return password_hasher.verify(hashed_password, plain_password)
    except (VerifyMismatchError, Exception):
        return False


def create_access_token(user_id: int, email: str, is_demo: bool = False) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user_id),
        "email": email,
        "demo": is_demo,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=settings.jwt_expire_minutes)).timestamp()),
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> dict:
    try:
        return jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
    except jwt.ExpiredSignatureError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired. Please sign in again.",
        ) from exc
    except jwt.InvalidTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token.",
        ) from exc


class SlidingWindowRateLimiter:
    """In-memory per-IP / per-route sliding window rate limiter."""

    def __init__(self, max_requests: int = 90, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._hits: Dict[str, Deque[float]] = defaultdict(deque)
        self._lock = threading.Lock()

    def check(self, key: str, limit: Optional[int] = None) -> None:
        cap = limit if limit is not None else self.max_requests
        now = time.monotonic()
        cutoff = now - self.window_seconds
        with self._lock:
            bucket = self._hits[key]
            while bucket and bucket[0] <= cutoff:
                bucket.popleft()
            if len(bucket) >= cap:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Rate limit exceeded. Please wait briefly before trying again.",
                )
            bucket.append(now)

    def reset(self) -> None:
        with self._lock:
            self._hits.clear()


rate_limiter = SlidingWindowRateLimiter(max_requests=settings.rate_limit_per_minute, window_seconds=60)


def enforce_rate_limit(request: Request, bucket_suffix: str = "global", limit: Optional[int] = None) -> None:
    client_host = request.client.host if request.client else "unknown"
    key = f"{client_host}:{bucket_suffix}"
    rate_limiter.check(key, limit=limit)


def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    if not credentials or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required.",
        )
    payload = decode_access_token(credentials.credentials)
    try:
        user_id = int(payload["sub"])
    except (KeyError, TypeError, ValueError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token subject.",
        ) from exc
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authenticated user no longer exists.",
        )
    return user


def get_current_business(
    request: Request,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Tuple[User, Business]:
    requested_biz_id = request.headers.get("X-Business-Id")
    business: Optional[Business] = None
    if requested_biz_id:
        try:
            biz_id_int = int(requested_biz_id)
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid X-Business-Id header.",
            ) from exc
        business = (
            db.query(Business)
            .filter(Business.id == biz_id_int, Business.owner_id == user.id)
            .first()
        )
        if not business:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied for requested business workspace.",
            )
    else:
        business = db.query(Business).filter(Business.owner_id == user.id).order_by(Business.id.asc()).first()

    if not business:
        business = Business(
            owner_id=user.id,
            name=f"{user.full_name}'s Business",
            industry="Small Business",
            employee_count=5,
            city="Guwahati",
            is_demo_workspace=user.is_demo,
        )
        db.add(business)
        db.commit()
        db.refresh(business)
    return user, business


def record_audit_log(
    db: Session,
    action: str,
    resource_type: str,
    summary: str,
    user_id: Optional[int] = None,
    business_id: Optional[int] = None,
    resource_id: Optional[str] = None,
    request: Optional[Request] = None,
) -> None:
    ip_address = request.client.host if request and request.client else None
    entry = AuditLog(
        user_id=user_id,
        business_id=business_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        summary=summary[:255],
        ip_address=ip_address,
    )
    db.add(entry)
    db.commit()

