from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import uuid4
from datetime import datetime

from app.core.ownership import is_parent_of_child, is_teacher_of_child
from app.db.session import get_db
from app.schemas.event import EventCreate, EventResponse
from app.models.event import Event
from app.core.dependencies import get_current_user
from app.core.event_rules import ROLE_EVENT_MAP

router = APIRouter(prefix="/events", tags=["Events"])
@router.post("/", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
def submit_event(
    event: EventCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    role = current_user["role"]
    user_id = current_user["user_id"]

    # 1️⃣ Validate event type by role
    if event.event_type not in ROLE_EVENT_MAP.get(role, set()):
        raise HTTPException(
            status_code=403,
            detail="Event type not allowed for this role"
        )

    # 2️⃣ Ownership rules
    if role == "student":
        if event.child_id != user_id:
            raise HTTPException(
                status_code=403,
                detail="Students can submit events only for themselves"
            )

    elif role == "admin":
        if event.child_id is not None:
            raise HTTPException(
                status_code=403,
                detail="Admin events must not have child_id"
            )

    elif role == "parent":
        if not event.child_id:
            raise HTTPException(
                status_code=400,
                detail="child_id is required for parent events"
            )
        if not is_parent_of_child(db, user_id, event.child_id):
            raise HTTPException(
                status_code=403,
                detail="Parent not mapped to this child"
            )

    elif role == "teacher":
        if not event.child_id:
            raise HTTPException(
                status_code=400,
                detail="child_id is required for teacher events"
            )
        if not is_teacher_of_child(db, user_id, event.child_id):
            raise HTTPException(
                status_code=403,
                detail="Teacher not assigned to this student's class"
            )

    # 3️⃣ Persist raw event (IMMUTABLE)
    db_event = Event(
        id=str(uuid4()),
        child_id=event.child_id,
        event_type=event.event_type,
        payload=event.payload,
        timestamp=datetime.utcnow(),          # SERVER TIME
        processed=False,                      # REQUIRED
        created_at=datetime.utcnow(),
        actor_id=user_id
    )

    db.add(db_event)
    db.commit()
    db.refresh(db_event)

    return db_event
