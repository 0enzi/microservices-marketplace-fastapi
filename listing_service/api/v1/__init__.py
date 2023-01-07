from fastapi import APIRouter

from .listings import listing_routes

api_router = APIRouter()
api_router.include_router(listing_routes.router, prefix="/listings", tags=["Listings"])

