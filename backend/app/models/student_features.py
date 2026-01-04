from sqlalchemy import Column, String, Float, DateTime
from datetime import datetime
from sqlalchemy.sql import func
from app.db.base import Base


class StudentFeatures(Base):
    __tablename__ = "student_features"

    child_id = Column(String, primary_key=True, index=True)

    attendance_7d = Column(Float)
    attendance_30d = Column(Float)

    homework_7d = Column(Float)
    homework_30d = Column(Float)

    test_score_7d = Column(Float)
    test_score_30d = Column(Float)

    attendance_delta = Column(Float)
    homework_delta = Column(Float)
    test_score_delta = Column(Float)

    attendance_norm = Column(Float)
    homework_norm = Column(Float)
    test_score_norm = Column(Float)

    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )
