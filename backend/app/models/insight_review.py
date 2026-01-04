from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.db.base import Base

class InsightReview(Base):
    __tablename__ = "insight_reviews"

    id = Column(Integer, primary_key=True)
    child_id = Column(String, nullable=False)
    reviewer_id = Column(String, nullable=False)
    reviewer_role = Column(String, nullable=False)
    reviewed_at = Column(DateTime, default=datetime.utcnow)
