from email.policy import default
from sqlalchemy import Column, String, Boolean, DateTime,func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from datetime import datetime
import uuid

from app.db.base import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    child_id = Column(UUID(as_uuid=True), nullable=False)

    event_type = Column(String, nullable=False)
    payload = Column(JSONB, nullable=False)

    # ✅ FIX IS HERE
    timestamp = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )

    processed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
