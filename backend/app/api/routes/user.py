from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import dbConnDep, currentUser
from app.core.db import user_table
from app.core.security import create_access_token, hash_password, verify_password
from app.crud import find_user_by_email
from app.models import Token, UserIn, User

router = APIRouter()


@router.get("/welcome")
async def greeting():
    return {"message": "Hello, welcome to the User API!"}


@router.post("/user", status_code=201)
async def register_user(user_in: UserIn, db_conn: dbConnDep):
    user = find_user_by_email(db_conn, user_in.email)
    if user:
        raise HTTPException(status_code=400, detail="User with this email already exists, please user another email")
    try:
        stmt = user_table.insert().values(
            username=user_in.username,
            email=user_in.email,
            password_hash=hash_password(user_in.password.get_secret_value()),
        )
        result = db_conn.execute(stmt)
        db_conn.commit()
    except Exception:
        raise HTTPException(status_code=500, detail="something went wrong, try again.")
    return {
        "success": True,
        "message": "registration successfull",
        "id": result.inserted_primary_key[0],
    }


@router.post("/token", response_model=Token)
def login_access_token(
    db_conn: dbConnDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = find_user_by_email(db_conn, form_data.username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = create_access_token(user.uid)
    return Token(access_token=token)


@router.get("/users/me", response_model=User)
def get_logged_in_user_profile(current_user: currentUser):
    return User.model_validate(current_user)


@router.delete("/users/me")
async def delete_logged_in_user(db_conn: dbConnDep, current_user: currentUser):
    stmt = user_table.delete().where(user_table.c.uid == current_user.uid)
    try:
        db_conn.execute(stmt)
        db_conn.commit()
    except:
        raise HTTPException(
            status_code=500,
            detail="an unexpected error occured deleting your account."
        )
    return {"message": "User deleted successfully"}
