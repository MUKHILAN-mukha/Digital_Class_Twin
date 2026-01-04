from pydantic import BaseModel
from typing import Dict
from datetime import datetime


class RiskInsightOut(BaseModel):
    child_id: str
    risk_level: str
    scores: Dict[str, float]
    explanation: Dict
    last_updated: datetime

    class Config:
        from_attributes = True
