from datetime import datetime, timedelta
from jose import jwt
from app.core.config import settings


def create_access_token(data: dict) -> str:
    """
    Creates a JWT access token with expiry.
    Bound payload is expected to already include:
    - user_id
    - role
    - session_id
    """
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
