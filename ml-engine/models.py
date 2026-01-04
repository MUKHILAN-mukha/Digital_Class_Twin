from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Boolean, DateTime, Float
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime

Base = declarative_base()


class Event(Base):
    __tablename__ = "events"

    id = Column(String, primary_key=True)
    child_id = Column(String)
    event_type = Column(String)
    payload = Column(JSONB)
    created_at = Column(DateTime)   # ✅ FIXED (was timestamp)
    processed = Column(Boolean, default=False)


class DigitalTwin(Base):
    __tablename__ = "digital_twins"

    child_id = Column(String, primary_key=True)

    academic_score = Column(Float)
    attendance_score = Column(Float)
    behavior_score = Column(Float)

    risk_level = Column(String)
    explanation = Column(JSONB)

    last_updated = Column(DateTime, default=datetime.utcnow)
