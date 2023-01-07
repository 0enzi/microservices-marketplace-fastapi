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

# @router.get("/{user_id}")
# def get_user(request: Request, user_id: str):
#     # Check if the user is in the cache
#     cache_key = CACHE_KEY_PREFIX + user_id
#     cached_user = request.app.redis_client.get(cache_key)
#     if cached_user:
#         # Return the user from the cache
#         return json.loads(cached_user)

#     # If the user is not in the cache, get it from the database
#     user = request.app.database["users"].find_one({"_id": user_id})
#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")

#     # Add the user to the cache and return it
#     request.app.redis_client.set(cache_key, json.dumps(user))
#     return user


# @router.post("/", response_description="Create a new user", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
# async def create_user(request: Request, user: UserForm = Body(...)):
    
#     existing_user = request.app.database["users"].find_one({"email": user.email})
#     if existing_user is not None:
#         raise HTTPException(status_code=400, detail="A user with this email already exists")


#     # Parse and autofill remaining fields before saving to db
#     user_obj = {
#         "account_info": {},
#         "username": user.email.split("@")[0],
#         "password": get_password_hash(user.password),
#         "created_at": datetime.datetime.now().timestamp(),
#         "account_type_id": "USER",
#         "is_super_admin": False,
#         "status": True,
#         "email_verified": False,
#         "phone_verified": False,
#     }

    

#     user_obj.update(user.dict())
    
#     # Insert the new user into the database and Cache using redis
#     new_user = request.app.database["users"].insert_one(user_obj)
#     user_json = dumps(user_obj)


#     cache_key = CACHE_KEY_PREFIX + str(new_user.inserted_id)
    
#     print("USER KEY", cache_key, "USER KEY") 
    
#     request.app.redis_client.set(cache_key, user_json)

#     created_user = request.app.database["users"].find_one({"_id": loads(user_json).get("_id")})
#     print(loads(user_json)['_id'])
    
#     return created_user


# @router.put("/{user_id}")
# def update_user(request: Request, user_id: str, user: dict):

#     result = request.app.database["users"].update_one({"_id": user_id}, {"$set": user})
#     if result.modified_count == 0:
#         raise HTTPException(status_code=404, detail="User not found")


#     cache_key = CACHE_KEY_PREFIX + user_id
#     request.app.redis_client.set(cache_key, json.dumps(user))

# @router.delete("/{user_id}")
# def delete_user(request: Request,user_id: str):
   
#     result = request.app.database["users"].delete_one({"_id": user_id})
#     if result.deleted_count == 0:
#         raise HTTPException(status_code=404, detail="User not found")

  
#     cache_key = CACHE_KEY_PREFIX + user_id
#     request.app.redis_client.delete(cache_key)


""""

AUTHENTICATION

"""

# @router.post("/login")
# def login(request: Request, user: UsernamePasswordForm = Body(...)):
#     # Get the user from the database
#     user = request.app.database["users"].find_one({"email": user.email})
#     if user is None:
#         raise HTTPException(status_code=400, detail="Incorrect email or password")

#     # Verify the password
#     if not verify_password(user["password"], user.password):
#         raise HTTPException(status_code=400, detail="Incorrect email or password")

#     # Generate a JWT token and return it
#     return {"access_token": create_access_token(user["_id"], request.app.jwt_secret, request.app.jwt_algorithm)}


"""
CATEGORY OPERATIONS
"""
