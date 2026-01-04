from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.schemas.profile import ProfileUpdate, PasswordChange
from app.models.user import User
from app.core.security import verify_password, hash_password

router = APIRouter(prefix="/profile", tags=["Profile"])
@router.get("/me")
def get_my_profile(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    user = db.query(User).filter(
        User.id == current_user["user_id"]
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "user_id": user.id,
        "role": user.role,
        "email": user.email,
        "full_name": user.full_name,
        "phone": user.phone,
        "created_at": user.created_at,
    }

@router.put("/me")
def update_my_profile(
    payload: ProfileUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    user = db.query(User).filter(
        User.id == current_user["user_id"]
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if payload.name is not None:
        user.name = payload.name

    if payload.email is not None:
        user.email = payload.email

    if payload.phone is not None:
        user.phone = payload.phone

    db.commit()
    db.refresh(user)

    return {
        "status": "profile_updated",
        "user_id": user.id
    }
@router.post("/change-password")
def change_password(
    payload: PasswordChange,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    user = db.query(User).filter(
        User.id == current_user["user_id"]
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(payload.old_password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect old password")

    user.hashed_password = hash_password(payload.new_password)

    db.commit()

    return {
        "status": "password_changed",
        "message": "Please login again"
    }
