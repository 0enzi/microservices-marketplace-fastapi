import json
import datetime
from bson.json_util import dumps, loads

from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi import APIRouter, Depends, status, Response, HTTPException, Request



router = APIRouter()

CACHE_KEY_PREFIX = "listing:"


'''

BASIC CRUD OPERATIONS FOR LISTINGS

'''

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


@router.post("/", response_description="Create a new listing", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_listing(request: Request, listing: UserForm = Body(...)):
    
    existing_listing = request.app.database["listings"].find_one({"email": listing.email})
    if existing_listing is not None:
        raise HTTPException(status_code=400, detail="A listing with this email already exists")


    # Parse and autofill remaining fields before saving to db
    listing_obj = {
        "account_info": {},
        "listingname": listing.email.split("@")[0],
        "password": get_password_hash(listing.password),
        "created_at": datetime.datetime.now().timestamp(),
        "account_type_id": "USER",
        "is_super_admin": False,
        "status": True,
        "email_verified": False,
        "phone_verified": False,
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
