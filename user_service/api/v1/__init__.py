from fastapi import APIRouter

from users import user_routes

api_router = APIRouter()
api_router.include_router(user_routes.router, prefix="/user", tags=["Users"])

