import json
import datetime, time
import random
import string
from typing import List
from bson.json_util import dumps, loads

from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi import APIRouter, Depends, status, Response, HTTPException, Request

from models.review import ListingInDB as Listing
from models.review import ListingForm, ListingUpdate, ListingResponse

router = APIRouter()

CACHE_KEY_PREFIX = "review:"



# get all reviews
@router.get("/review/{review_id}", response_description="List all reviews in review") #, response_model=List[ListingResponse])
def get_reviews_by_review(review_id: str, request: Request):
    pass


@router.get("/review/{review_id}")
def get_review(request: Request, review_id: str):
    # Check if the review is in the cache
    cache_key = CACHE_KEY_PREFIX + review_id
    cached_review = request.app.redis_client.get(cache_key)
    if cached_review:
        # Return the review from the cache
        return json.loads(cached_review)

    # If the review is not in the cache, get it from the database
    review = request.app.database["reviews"].find_one({"_id": review_id})
    if review is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Add the review to the cache and return it
    request.app.redis_client.set(cache_key, json.dumps(review))
    return review


@router.post("/", response_description="Create a new review", status_code=status.HTTP_201_CREATED, response_model=ListingResponse)
async def create_review(request: Request, review: ListingForm = Body(...)):
    user_id = "5f9f1b9b9b9b9b9b9b9b9b9b" # random user

    """
    user_id: str
    review: str
    rating: float
    timestamp: str

    class Config:
        collection = "reviews"
    """
    # Parse and autofill remaining fields before saving to db
    review_obj = {
        "user_id": user_id,
        "review": review.review,
        "rating": review.rating,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    }

    

    review_obj.update(review.dict())
    
    # Insert the new review into the database and Cache using redis
    new_review = request.app.database["reviews"].insert_one(review_obj)
    review_json = dumps(review_obj)


    cache_key = CACHE_KEY_PREFIX + str(new_review.inserted_id)
    
    print("USER KEY", cache_key, "USER KEY") 
    
    request.app.redis_client.set(cache_key, review_json)

    created_review = request.app.database["reviews"].find_one({"_id": loads(review_json).get("_id")})
    print(loads(review_json)['_id'])
    
    return created_review


@router.put("/{review_id}")
def update_review(request: Request, review_id: str, review: dict):

    result = request.app.database["reviews"].update_one({"_id": review_id}, {"$set": review})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found")


    cache_key = CACHE_KEY_PREFIX + review_id
    request.app.redis_client.set(cache_key, json.dumps(review))


@router.delete("/{review_id}")
def delete_review(request: Request,review_id: str):
   
    result = request.app.database["reviews"].delete_one({"_id": review_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

  
    cache_key = CACHE_KEY_PREFIX + review_id
    request.app.redis_client.delete(cache_key)
