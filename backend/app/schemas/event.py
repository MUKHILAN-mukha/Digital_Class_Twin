from pydantic import BaseModel, Field, validator
from typing import Dict, Optional, Literal, Any
from datetime import datetime


# --------------------
# Payload Schemas
# --------------------

class AttendancePayload(BaseModel):
    present: bool


class TestPayload(BaseModel):
    score: float = Field(..., ge=0, le=100)


class BehaviorPayload(BaseModel):
    note: str


# --------------------
# Event Create Schema
# --------------------

class EventCreate(BaseModel):
    child_id: Optional[str]
    event_type: Literal["attendance", "test", "behavior"]
    payload: Dict[str, Any]

    @validator("payload")
    def validate_payload_by_type(cls, payload, values):
        event_type = values.get("event_type")

        if event_type == "attendance":
            AttendancePayload(**payload)
        elif event_type == "test":
            TestPayload(**payload)
        elif event_type == "behavior":
            BehaviorPayload(**payload)
        else:
            raise ValueError("Unsupported event type")

        return payload


# --------------------
# Event Response Schema
# --------------------

class EventResponse(BaseModel):
    id: str
    child_id: Optional[str]
    event_type: str
    payload: Dict
    timestamp: datetime
    processed: bool

    class Config:
        orm_mode = True
