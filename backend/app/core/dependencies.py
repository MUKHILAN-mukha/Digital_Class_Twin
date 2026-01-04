from fastapi import HTTPException, Security, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError, ExpiredSignatureError
from sqlalchemy.orm import Session
from datetime import datetime
from dotenv import load_dotenv
import os

from app.db.session import get_db
from app.models.user import User
from app.models.user_session import UserSession

# Load environment variables
load_dotenv()

bearer = HTTPBearer()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY not set")


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(bearer),
    db: Session = Depends(get_db),
):
    try:
        payload = jwt.decode(
            credentials.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        user_id = payload.get("user_id")
        session_id = payload.get("session_id")

        if not user_id or not session_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
            )

        # ✅ FIX: Use UserSession.id (NOT session_id)
        session = (
            db.query(UserSession)
            .filter(
                UserSession.id == session_id,
                UserSession.user_id == user_id,
                UserSession.is_active == True,
            )
            .first()
        )

        if not session:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Session expired or invalid",
            )

        # Update activity
        session.last_seen_at = datetime.utcnow()
        db.commit()

        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )

        return {
            "user_id": str(user.id),
            "role": user.role,
        }

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
        )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
