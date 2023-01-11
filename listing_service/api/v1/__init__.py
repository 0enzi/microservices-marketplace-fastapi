from fastapi import APIRouter

from .listings import listing_routes
from .categories import category, sub_category

api_router = APIRouter()
api_router.include_router(listing_routes.router, prefix="/listings", tags=["Listings"])
api_router.include_router(category.router, prefix="/categories", tags=["Categories"])
api_router.include_router(sub_category.router, prefix="/sub_categories", tags=["Sub Categories"])
