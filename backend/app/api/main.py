from fastapi import APIRouter

from app.api.routes import oauth, user

api_router = APIRouter()


api_router.include_router(user.router, prefix="/api")
api_router.include_router(oauth.router, prefix="/auth")
