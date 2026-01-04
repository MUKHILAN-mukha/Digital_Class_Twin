from sqlalchemy import Column, String, Float, DateTime, JSON
from datetime import datetime
from app.db.base import Base


class DigitalTwin(Base):
    __tablename__ = "digital_twins"

    child_id = Column(String, primary_key=True)

    academic_score = Column(Float, default=0.0)
    attendance_score = Column(Float, default=0.0)
    behavior_score = Column(Float, default=0.0)

    # 🔴 THIS WAS MISSING
    twin_state = Column(String, default="stable")

    risk_level = Column(String, default="unknown")

    derived_metrics = Column(JSON, default=dict)
    explanation = Column(JSON, default=dict)

    last_updated = Column(DateTime, default=datetime.utcnow)
    last_updated_at = Column(DateTime, default=datetime.utcnow)
