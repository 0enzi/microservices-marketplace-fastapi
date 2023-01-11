import json
import datetime, time
import random
import string
from typing import List
from bson.json_util import dumps, loads

from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi import APIRouter, Depends, status, Response, HTTPException, Request

from models.category import SubCategoryInDB as SubCategory
from models.category import SubCategoryForm, SubCategoryUpdate, SubCategoryResponse

router = APIRouter()

CACHE_KEY_PREFIX = "sub_category:"



def generate_reference():
    # Generate a random string of length 8
    reference = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    return "ieloro:"+reference


# get all sub_categories
@router.get("/", response_description="List all sub_categories") #, response_model=List[SubCategoryResponse])
def get_sub_categories(request: Request):
    sub_category_dict = []
    sub_categories = request.app.database["sub_categories"].find()

    for sub_category in sub_categories:
        sub_category['id'] = str(sub_category['_id'])
        sub_category_dict.append(SubCategoryResponse(**sub_category))
  
    return sub_category_dict


@router.get("/{sub_category_id}")
def get_sub_category(request: Request, sub_category_id: str):
    # Check if the sub_category is in the cache
    cache_key = CACHE_KEY_PREFIX + sub_category_id
    cached_sub_category = request.app.redis_client.get(cache_key)
    if cached_sub_category:
        # Return the sub_category from the cache
        return json.loads(cached_sub_category)

    # If the sub_category is not in the cache, get it from the database
    sub_category = request.app.database["sub_categories"].find_one({"_id": sub_category_id})
    if sub_category is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Add the sub_category to the cache and return it
    request.app.redis_client.set(cache_key, json.dumps(sub_category))
    return sub_category


@router.post("/", response_description="Create a new sub_category", status_code=status.HTTP_201_CREATED, response_model=SubCategoryResponse)
async def create_sub_category(request: Request, sub_category: SubCategoryForm = Body(...)):
    user_id = "5f9f1b9b9b9b9b9b9b9b9b9b" # random user

    """
    title: str
    slug: str
    description: str
    seo_tag_title: str
    seo_tag_description: str
    seo_tag_keywords: list
    active: str
    created_at: str
    updated_at: str
    listings: list
    sub_categories: list
    """

    # Parse and autofill remaining fields before saving to db
    sub_category_obj = {
        "title": sub_category.title,
        "slug": sub_category.slug,
        "description": sub_category.description,
        "seo_tag_title": sub_category.seo_tag_title,
        "seo_tag_description": sub_category.seo_tag_description,
        "seo_tag_keywords": sub_category.seo_tag_keywords,
        "active": True,
        "created_at": datetime.datetime.utcnow(),
        "updated_at": datetime.datetime.utcnow(),
        "listings": [],
        "sub_categories": [],

    }

    

    sub_category_obj.update(sub_category.dict())
    
    # Insert the new sub_category into the database and Cache using redis
    new_sub_category = request.app.database["sub_categories"].insert_one(sub_category_obj)
    sub_category_json = dumps(sub_category_obj)


    cache_key = CACHE_KEY_PREFIX + str(new_sub_category.inserted_id)
    
    print("USER KEY", cache_key, "USER KEY") 
    
    request.app.redis_client.set(cache_key, sub_category_json)

    created_sub_category = request.app.database["sub_categories"].find_one({"_id": loads(sub_category_json).get("_id")})
    print(loads(sub_category_json)['_id'])
    
    return created_sub_category


@router.put("/{sub_category_id}")
def update_sub_category(request: Request, sub_category_id: str, sub_category: dict):

    result = request.app.database["sub_categories"].update_one({"_id": sub_category_id}, {"$set": sub_category})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found")


    cache_key = CACHE_KEY_PREFIX + sub_category_id
    request.app.redis_client.set(cache_key, json.dumps(sub_category))


@router.delete("/{sub_category_id}")
def delete_sub_category(request: Request,sub_category_id: str):
   
    result = request.app.database["sub_categories"].delete_one({"_id": sub_category_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

  
    cache_key = CACHE_KEY_PREFIX + sub_category_id
    request.app.redis_client.delete(cache_key)
