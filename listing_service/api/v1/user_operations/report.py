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
    category = request.app.database["categories"].find_one({"_id": category_id})
    if category is None:
        raise HTTPException(status_code=404, detail="User not found")

    return category



@router.get("/{category_id}")
def get_category(request: Request, category_id: str):
    # Check if the category is in the cache
    cache_key = CACHE_KEY_PREFIX + category_id
    cached_category = request.app.redis_client.get(cache_key)
    if cached_category:
        # Return the category from the cache
        return json.loads(cached_category)

    # If the category is not in the cache, get it from the database
    category = request.app.database["categories"].find_one({"_id": category_id})
    if category is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Add the category to the cache and return it
    request.app.redis_client.set(cache_key, json.dumps(category))
    return category


@router.post("/", response_description="Create a new category", status_code=status.HTTP_201_CREATED, response_model=CategoryResponse)
async def create_category(request: Request, category: CategoryForm = Body(...)):

  
    # Parse and autofill remaining fields before saving to db
    category_obj = {
        "name": category.name,
        "seo_tag_title": category.seo_tag_title,
        "seo_tag_description": category.seo_tag_description,
        "seo_tag_keywords": category.seo_tag_keywords,
    }


    category_obj.update(category.dict())
    
    # Insert the new category into the database and Cache using redis
    new_category = request.app.database["categories"].insert_one(category_obj)
    category_json = dumps(category_obj)


    cache_key = CACHE_KEY_PREFIX + str(new_category.inserted_id)
    
    print("USER KEY", cache_key, "USER KEY") 
    
    request.app.redis_client.set(cache_key, category_json)

    created_category = request.app.database["categories"].find_one({"_id": loads(category_json).get("_id")})
    print(loads(category_json)['_id'])
    
    return created_category


@router.put("/{category_id}")
def update_category(request: Request, category_id: str, category: dict):

    result = request.app.database["categories"].update_one({"_id": category_id}, {"$set": category})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found")


    cache_key = CACHE_KEY_PREFIX + category_id
    request.app.redis_client.set(cache_key, json.dumps(category))


@router.delete("/{category_id}")
def delete_category(request: Request,category_id: str):
   
    result = request.app.database["categories"].delete_one({"_id": category_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

  
    cache_key = CACHE_KEY_PREFIX + category_id
    request.app.redis_client.delete(cache_key)
