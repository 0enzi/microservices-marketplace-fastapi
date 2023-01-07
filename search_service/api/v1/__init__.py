from fastapi import APIRouter

import email_routes


api_router = APIRouter()
api_router.include_router(email_routes.router, prefix="/email", tags=["Emails"])

