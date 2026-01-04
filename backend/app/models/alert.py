from sqlalchemy import Column, String, Boolean, DateTime, JSON
from datetime import datetime
from app.db.base import Base


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(String, primary_key=True)
    child_id = Column(String, nullable=False)

    alert_type = Column(String, nullable=False)     # e.g. "risk"
    category = Column(String, nullable=True)        # academic / attendance / behavior
    severity = Column(String, nullable=False)       # low / medium / high
    target_role = Column(String, nullable=True)     # student / parent / teacher

    message = Column(String, nullable=False)
    context = Column(JSON, default=dict, nullable=False)

    resolved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)
