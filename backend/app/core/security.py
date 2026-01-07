from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

from app.core.config import settings

pwd_hash = PasswordHash.recommended()


def hash_password(plain_password: str) -> str:
    return pwd_hash.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_hash.verify(plain_password, hashed_password)


def get_access_token_expiration_minutes() -> int:
    return settings.ACCESS_TOKEN_EXPIRES_AT or 1440


def create_access_token(subject: str) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=get_access_token_expiration_minutes()
    )
    jwt_data = {"exp": expires_at, "sub": str(subject)}
    token = jwt.encode(
        payload=jwt_data,
        key=settings.JWT_SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    return token
