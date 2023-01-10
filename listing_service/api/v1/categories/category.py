import json
import datetime, time
import random
import string
from typing import List
from bson.json_util import dumps, loads

from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi import APIRouter, Depends, status, Response, HTTPException, Request

from models.category import CategoryInDB as Category
from models.category import CategoryForm, CategoryUpdate, CategoryResponse

router = APIRouter()

CACHE_KEY_PREFIX = "category:"


'''

BASIC CRUD OPERATIONS FOR LISTINGS

'''

def generate_reference():
    # Generate a random string of length 8
    reference = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    return "ieloro:"+reference


# get all categories
@router.get("/", response_description="List all categories") #, response_model=List[CategoryResponse])
def get_categories(request: Request):
    category_dict = []
    categories = request.app.database["categories"].find()

    for category in categories:
        category['id'] = str(category['_id'])
        category_dict.append(CategoryResponse(**category))
  
    return category_dict


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
    user_id = "5f9f1b9b9b9b9b9b9b9b9b9b" # random user

    """
    Categories
    account_id: str
    display_images: List[str]
    title: str
    views: int
    reference: str
    location: str
    category_id: str
    additional_details: dict
    promoted: bool
    status: str # (activated, unactivated, pending)
    created_at: str
    updated_at: str
    """
    # Parse and autofill remaining fields before saving to db
    category_obj = {
        "account_id": user_id,
        "display_images": category.display_images,
        "title": category.title,
        "views": 0,
        "reference": generate_reference(),
        "location": category.location,
        "category_id": category.category_id,
        "additional_details": category.additional_details,
        "promoted": category.promoted,
        "status": "activated",
        "created_at": time.time(),
        "updated_at": time.time()
    

    }

    

    category_obj.update(category.dict())
    
    # Insert the new category into the database and Cache using redis
    new_category = request.app.database["categorys"].insert_one(category_obj)
    category_json = dumps(category_obj)


    cache_key = CACHE_KEY_PREFIX + str(new_category.inserted_id)
    
    print("USER KEY", cache_key, "USER KEY") 
    
    request.app.redis_client.set(cache_key, category_json)

    created_category = request.app.database["categorys"].find_one({"_id": loads(category_json).get("_id")})
    print(loads(category_json)['_id'])
    
    return created_category


@router.put("/{category_id}")
def update_category(request: Request, category_id: str, category: dict):

    result = request.app.database["categorys"].update_one({"_id": category_id}, {"$set": category})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found")


    cache_key = CACHE_KEY_PREFIX + category_id
    request.app.redis_client.set(cache_key, json.dumps(category))


@router.delete("/{category_id}")
def delete_category(request: Request,category_id: str):
   
    result = request.app.database["categorys"].delete_one({"_id": category_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

  
    cache_key = CACHE_KEY_PREFIX + category_id
    request.app.redis_client.delete(cache_key)


""""

AUTHENTICATION

"""

# @router.post("/login")
# def login(request: Request, category: UsernamePasswordForm = Body(...)):
#     # Get the category from the database
#     category = request.app.database["categorys"].find_one({"email": category.email})
#     if category is None:
#         raise HTTPException(status_code=400, detail="Incorrect email or password")

#     # Verify the password
#     if not verify_password(category["password"], category.password):
#         raise HTTPException(status_code=400, detail="Incorrect email or password")

#     # Generate a JWT token and return it
#     return {"access_token": create_access_token(category["_id"], request.app.jwt_secret, request.app.jwt_algorithm)}


"""
CATEGORY OPERATIONS
"""
