from sqlalchemy import Column, String, DateTime, Boolean
from datetime import datetime
import uuid

from app.db.base import Base


class UserSession(Base):
    __tablename__ = "user_sessions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, index=True, nullable=False)

    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    device = Column(String, nullable=True)

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    last_seen_at = Column(DateTime, default=datetime.utcnow)
