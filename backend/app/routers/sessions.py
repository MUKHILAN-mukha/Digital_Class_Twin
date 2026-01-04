from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.models.user_session import UserSession

router = APIRouter(
    prefix="/profile/sessions",
    tags=["Sessions"]
)


@router.get("")
def get_my_sessions(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    View all login sessions for the current user
    """

    sessions = (
        db.query(UserSession)
        .filter(UserSession.user_id == current_user["user_id"])
        .order_by(UserSession.created_at.desc())
        .all()
    )

    return [
        {
            "session_id": s.session_id,
            "ip_address": s.ip_address,
            "device": s.device,
            "user_agent": s.user_agent,
            "is_active": s.is_active,
            "created_at": s.created_at,
            "last_seen_at": s.last_seen_at,
        }
        for s in sessions
    ]


@router.post("/logout")
def logout_current_session(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Logout the most recent active session
    """

    session = (
        db.query(UserSession)
        .filter(
            UserSession.user_id == current_user["user_id"],
            UserSession.is_active == True
        )
        .order_by(UserSession.created_at.desc())
        .first()
    )

    if not session:
        raise HTTPException(status_code=404, detail="Active session not found")

    session.is_active = False
    session.last_seen_at = datetime.utcnow()

    db.commit()

    return {"status": "logged_out"}


@router.post("/logout-all")
def logout_all_sessions(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Logout all active sessions for the user
    """

    (
        db.query(UserSession)
        .filter(
            UserSession.user_id == current_user["user_id"],
            UserSession.is_active == True
        )
        .update(
            {
                "is_active": False,
                "last_seen_at": datetime.utcnow()
            }
        )
    )

    db.commit()

    return {"status": "all_sessions_logged_out"}
