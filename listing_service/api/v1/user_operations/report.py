import json
import datetime, time
import random
import string
from typing import List
from bson.json_util import dumps, loads

from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi import APIRouter, Depends, status, Response, HTTPException, Request

from models.category import Category
from models.category import CategoryForm, CategoryUpdate, CategoryResponse

router = APIRouter()

CACHE_KEY_PREFIX = "reports:"



# get all categories
@router.get("/report/{listing_id}", response_description="Get report by listing_id") #, response_model=List[CategoryResponse])
def get_reports_by_listing(request: Request, listing_id:str):

    # If the category is not in the cache, get it from the database
    listing = request.app.database["reports"].find_one({"listing_id":listing_id})
    if listing is None:
        raise HTTPException(status_code=404, detail="User not found")

    return listing

