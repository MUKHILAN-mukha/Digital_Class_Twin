from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime

class DigitalTwinOut(BaseModel):
    child_id: str
    academic_score: Optional[float]
    attendance_score: Optional[float]
    behavior_score: Optional[float]
    risk_level: str
    explanation: Dict
    last_updated: datetime

    class Config:
        from_attributes = True

