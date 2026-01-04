from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.event_processor import process_events
from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import hash_password
from app.dependencies import require_roles

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

@router.post("/create-user")
def create_user(
    email: str,
    password: str,
    role: str,
    admin=Depends(require_roles(["admin"]))
):
    db: Session = SessionLocal()

    if role not in ["student", "teacher", "parent", "admin"]:
        raise HTTPException(status_code=400, detail="Invalid role")

    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail="Email already exists")

    user = User(
        email=email,
        hashed_password=hash_password(password),
        role=role
    )

    db.add(user)
    db.commit()

    return {
        "message": "User created successfully",
        "email": email,
        "role": role
    }


# ✅ ADD THIS — NOTHING ELSE
@router.post("/process-events")
def process_pending_events(
    admin=Depends(require_roles(["admin"]))
):
    db: Session = SessionLocal()
    try:
        process_events(db)
        return {"status": "events processed"}
    finally:
        db.close()
