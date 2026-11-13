"""Employee Cyber Awareness training & quizzes API routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import AwarenessQuiz, QuizResult
from ..schemas import QuizResultOut, QuizSubmitRequest
from ..security import enforce_rate_limit, get_current_business, record_audit_log
from ..services.awareness_engine import get_awareness_overview, grade_quiz
from ..services.demo_seeder import ensure_quizzes_seeded


router = APIRouter(prefix="/api/awareness", tags=["Employee Awareness"])


@router.get("/overview")
def get_overview(
    language: str = Query("en", pattern="^(en|bn)$"),
    ctx=Depends(get_current_business),
    db: Session = Depends(get_db),
):
    ensure_quizzes_seeded(db)
    user, business = ctx
    content = get_awareness_overview(language)
    results = (
        db.query(QuizResult)
        .filter(QuizResult.business_id == business.id, QuizResult.user_id == user.id)
        .order_by(QuizResult.created_at.desc())
        .all()
    )
    best_by_slug = {}
    for res in results:
        quiz_row = db.query(AwarenessQuiz).filter(AwarenessQuiz.id == res.quiz_id).first()
        if not quiz_row:
            continue
        prev = best_by_slug.get(quiz_row.slug)
        if prev is None or res.percentage > prev:
            best_by_slug[quiz_row.slug] = res.percentage

    total_quizzes = len(content["quizzes"])
    completed_quizzes = len(best_by_slug)
    avg_score = round(sum(best_by_slug.values()) / completed_quizzes, 1) if completed_quizzes else 0.0

    content["progress"] = {
        "completed_quizzes": completed_quizzes,
        "total_quizzes": total_quizzes,
        "completion_percent": int(round((completed_quizzes / total_quizzes) * 100)) if total_quizzes else 0,
        "average_score": avg_score,
        "best_by_slug": best_by_slug,
        "recent_attempts": [
            {
                "id": r.id,
                "quiz_id": r.quiz_id,
                "score": r.score,
                "total_questions": r.total_questions,
                "percentage": r.percentage,
                "created_at": r.created_at.isoformat(),
            }
            for r in results[:10]
        ],
    }
    return content


@router.post("/quizzes/{slug}/submit", response_model=QuizResultOut, status_code=status.HTTP_201_CREATED)
def submit_quiz(
    slug: str,
    payload: QuizSubmitRequest,
    request: Request,
    language: str = Query("en", pattern="^(en|bn)$"),
    ctx=Depends(get_current_business),
    db: Session = Depends(get_db),
):
    enforce_rate_limit(request, bucket_suffix="quiz_submit", limit=30)
    ensure_quizzes_seeded(db)
    user, business = ctx

    quiz_row = db.query(AwarenessQuiz).filter(AwarenessQuiz.slug == slug).first()
    if not quiz_row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found.")

    try:
        graded = grade_quiz(slug, payload.answers, language=language)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc

    res = QuizResult(
        quiz_id=quiz_row.id,
        user_id=user.id,
        business_id=business.id,
        score=graded["score"],
        total_questions=graded["total_questions"],
        percentage=graded["percentage"],
        answers_summary=graded["answers_summary"],
    )
    db.add(res)
    db.commit()
    db.refresh(res)

    record_audit_log(
        db=db,
        action="awareness.quiz_completed",
        resource_type="quiz_result",
        resource_id=str(res.id),
        summary=f"Completed awareness quiz '{slug}' with {res.score}/{res.total_questions} ({res.percentage}%).",
        user_id=user.id,
        business_id=business.id,
        request=request,
    )

    return QuizResultOut(
        id=res.id,
        quiz_slug=slug,
        quiz_title=graded["quiz_title"],
        score=res.score,
        total_questions=res.total_questions,
        percentage=res.percentage,
        answers_summary=res.answers_summary,
        created_at=res.created_at,
    )

