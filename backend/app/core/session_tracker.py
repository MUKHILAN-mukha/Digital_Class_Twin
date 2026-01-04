from sqlalchemy.orm import Session
from datetime import datetime

from app.models.user_session import UserSession


def create_session(
    db: Session,
    user_id: str,
    ip: str | None,
    user_agent: str | None,
    device: str | None = None
):
    session = UserSession(
        user_id=user_id,
        ip_address=ip,
        user_agent=user_agent,
        device=device
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def touch_session(db: Session, user_id: str):
    db.query(UserSession) \
      .filter(
          UserSession.user_id == user_id,
          UserSession.is_active == True
      ) \
      .update({"last_seen_at": datetime.utcnow()})

    db.commit()
