from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class AlertOut(BaseModel):
    id: str
    child_id: str
    alert_type: str
    severity: str
    message: str
    context: Dict[str, Any]
    resolved: bool
    created_at: datetime
    resolved_at: Optional[datetime] = None

    class Config:
        from_attributes = True
