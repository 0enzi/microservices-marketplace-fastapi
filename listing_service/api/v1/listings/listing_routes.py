import json
import datetime, time
import random
import string
from typing import List
from bson.json_util import dumps, loads

from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi import APIRouter, Depends, status, Response, HTTPException, Request

from models.listing import ListingInDB as Listing
from models.listing import ListingForm, ListingUpdate, ListingResponse

router = APIRouter()

CACHE_KEY_PREFIX = "listing:"


'''

BASIC CRUD OPERATIONS FOR LISTINGS

'''

def generate_reference():
    # Generate a random string of length 8
    reference = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    return "ieloro:"+reference


# get all listings
@router.get("/", response_description="List all listings") #, response_model=List[ListingResponse])
def get_listings(request: Request):
    listing_dict = []
    listings = request.app.database["listings"].find()

    for listing in listings:
        listing['id'] = str(listing['_id'])
        del listing['_id']
        listing_dict.append(listing)
    return listing_dict


@router.get("/{listing_id}")
def get_listing(request: Request, listing_id: str):
    # Check if the listing is in the cache
    cache_key = CACHE_KEY_PREFIX + listing_id
    cached_listing = request.app.redis_client.get(cache_key)
    if cached_listing:
        # Return the listing from the cache
        return json.loads(cached_listing)

    # If the listing is not in the cache, get it from the database
    listing = request.app.database["listings"].find_one({"_id": listing_id})
    if listing is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Add the listing to the cache and return it
    request.app.redis_client.set(cache_key, json.dumps(listing))
    return listing


@router.post("/", response_description="Create a new listing", status_code=status.HTTP_201_CREATED, response_model=ListingResponse)
async def create_listing(request: Request, listing: ListingForm = Body(...)):
    user_id = "5f9f1b9b9b9b9b9b9b9b9b9b" # random user

    """
    Listings 
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
    listing_obj = {
        "account_id": user_id,
        "display_images": listing.display_images,
        "title": listing.title,
        "views": 0,
        "reference": generate_reference(),
        "location": listing.location,
        "category_id": listing.category_id,
        "additional_details": listing.additional_details,
        "promoted": listing.promoted,
        "status": "activated",
        "created_at": time.time(),
        "updated_at": time.time()
    

    }

    

    listing_obj.update(listing.dict())
    
    # Insert the new listing into the database and Cache using redis
    new_listing = request.app.database["listings"].insert_one(listing_obj)
    listing_json = dumps(listing_obj)


    cache_key = CACHE_KEY_PREFIX + str(new_listing.inserted_id)
    
    print("USER KEY", cache_key, "USER KEY") 
    
    request.app.redis_client.set(cache_key, listing_json)

    created_listing = request.app.database["listings"].find_one({"_id": loads(listing_json).get("_id")})
    print(loads(listing_json)['_id'])
    
    return created_listing


@router.put("/{listing_id}")
def update_listing(request: Request, listing_id: str, listing: dict):

    result = request.app.database["listings"].update_one({"_id": listing_id}, {"$set": listing})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found")


    cache_key = CACHE_KEY_PREFIX + listing_id
    request.app.redis_client.set(cache_key, json.dumps(listing))


@router.delete("/{listing_id}")
def delete_listing(request: Request,listing_id: str):
   
    result = request.app.database["listings"].delete_one({"_id": listing_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

  
    cache_key = CACHE_KEY_PREFIX + listing_id
    request.app.redis_client.delete(cache_key)


""""

AUTHENTICATION

"""

# @router.post("/login")
# def login(request: Request, listing: UsernamePasswordForm = Body(...)):
#     # Get the listing from the database
#     listing = request.app.database["listings"].find_one({"email": listing.email})
#     if listing is None:
#         raise HTTPException(status_code=400, detail="Incorrect email or password")

#     # Verify the password
#     if not verify_password(listing["password"], listing.password):
#         raise HTTPException(status_code=400, detail="Incorrect email or password")

#     # Generate a JWT token and return it
#     return {"access_token": create_access_token(listing["_id"], request.app.jwt_secret, request.app.jwt_algorithm)}


"""
CATEGORY OPERATIONS
"""
