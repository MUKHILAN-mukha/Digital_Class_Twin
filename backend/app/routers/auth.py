from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import hash_password, verify_password
from app.core.token import create_access_token
from app.core.session_tracker import create_session

router = APIRouter(prefix="/auth", tags=["Auth"])


class LoginRequest(BaseModel):
    email: str
    password: str


class SignupRequest(BaseModel):
    email: str
    password: str
    role: str


@router.post("/signup")
def signup(data: SignupRequest):
    db: Session = SessionLocal()
    try:
        if db.query(User).filter(User.email == data.email).first():
            raise HTTPException(status_code=400, detail="Email already exists")

        user = User(
            email=data.email,
            hashed_password=hash_password(data.password),
            role=data.role
        )
        db.add(user)
        db.commit()

        return {"message": "User created successfully"}
    finally:
        db.close()


@router.post("/login")
def login(data: LoginRequest, request: Request):
    db: Session = SessionLocal()
    try:
        user = db.query(User).filter(User.email == data.email).first()

        if not user or not verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # 🔐 Create DB session
        session = create_session(
            db=db,
            user_id=user.id,
            ip=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent"),
        )

        # 🔐 Bind JWT to DB session
        token = create_access_token({
            "user_id": user.id,
            "role": user.role,
            "session_id": str(session.id)
        })

        return {
            "access_token": token,
            "role": user.role
        }
    finally:
        db.close()
