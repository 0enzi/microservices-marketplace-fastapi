from fastapi import APIRouter, Depends, status, Response, HTTPException, Request
import json

router = APIRouter()

CACHE_KEY_PREFIX = "user:"

@router.get("/users/{user_id}")
def get_user(request: Request, user_id: str):
    # Check if the user is in the cache
    cache_key = CACHE_KEY_PREFIX + user_id
    cached_user = request.app.redis_client.get(cache_key)
    if cached_user:
        # Return the user from the cache
        return json.loads(cached_user)

    # If the user is not in the cache, get it from the database
    user = request.app.database["users"].find_one({"_id": user_id})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Add the user to the cache and return it
    request.app.redis_client.set(cache_key, json.dumps(user))
    return user

@router.post("/", response_description="Create a new user", status_code=status.HTTP_201_CREATED) # response_model=UserResponse)
async def create_user(request: Request, user: UserForm = Body(...)):
    
    existing_user = request.app.database["users"].find_one({"email": user.email})
    if existing_user is not None:
        raise HTTPException(status_code=400, detail="A user with this email already exists")


    # Parse and autofill remaining fields before saving to db
    user_obj = {
        "account_info": {},
        "username": user.email.split("@")[0],
        "password": get_password_hash(user.password),
        "created_at": datetime.datetime.now().timestamp(),
        "account_type_id": "USER",
        "is_super_admin": False,
        "status": True,
        "email_verified": False,
        "phone_verified": False,
    }

    

    user_obj.update(user.dict())
    
    # Insert the new user into the database and Cache using redis
    new_user = request.app.database["users"].insert_one(user_obj)
    user_json = json.dumps(user_obj)
    print(user_json)

    cache_key = CACHE_KEY_PREFIX + str(new_user.inserted_id)
    
    print("USER KEY", cache_key, "USER KEY") 
    
    request.app.redis_client.set(cache_key, user_json)
    created_user = request.app.database["users"].find_one({"_id": new_user.inserted_id})

    # return created_user
    return created_user


@router.put("/users/{user_id}")
def update_user(user_id: str, user: dict):
    # Update the user in the database
    result = request.app.database["users"].update_one({"_id": user_id}, {"$set": user})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    # Update the user in the cache
    cache_key = CACHE_KEY_PREFIX + user_id
    redis_client.set(cache_key, json.dumps(user))

@router.delete("/users/{user_id}")
def delete_user(user_id: str):
    # Delete the user from the database
    result = request.mongodbdatabase["users"].delete_one({"_id": user_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    # Delete the user from the cache
    cache_key = CACHE_KEY_PREFIX + user_id
    request.app.redis_client.delete(cache_key)