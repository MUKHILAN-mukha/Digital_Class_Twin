from sqlalchemy import Column, String, Numeric
from app.db.base import Base


class RiskScore(Base):
    __tablename__ = "risk_scores"

    child_id = Column(String, primary_key=True)

    attendance_risk = Column(Numeric)
    academic_risk = Column(Numeric)
    behavior_risk = Column(Numeric)
    volatility_risk = Column(Numeric)

    total_risk = Column(Numeric)
