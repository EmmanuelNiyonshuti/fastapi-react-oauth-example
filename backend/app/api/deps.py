from typing import Annotated, Generator

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import ExpiredSignatureError, InvalidTokenError
from sqlalchemy import Connection

from app.core.config import settings
from app.core.db import engine
from app.crud import find_user_by_id
from app.models import User

oath2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")


def credentials_exception(detail):
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_db() -> Generator[Connection, None, None]:
    with engine.connect() as conn:
        yield conn


dbConnDep = Annotated[Connection, Depends(get_db)]

accessTokenDep = Annotated[str, Depends(oath2_scheme)]


def get_current_user(db_conn: dbConnDep, token: accessTokenDep):
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
    except ExpiredSignatureError:
        raise credentials_exception("expired token")
    except InvalidTokenError:
        raise credentials_exception("Invalid token error")
    user = find_user_by_id(db_conn, int(payload["sub"]))
    if not user:
        raise credentials_exception("User does not exists")
    return user


currentUser = Annotated[User, Depends(get_current_user)]
