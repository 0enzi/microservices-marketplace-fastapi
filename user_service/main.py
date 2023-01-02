from fastapi import FastAPI, APIRouter, Body, Request, Response, HTTPException, status
from dotenv import dotenv_values
from pymongo import MongoClient
from routes import router as user_router


import datetime
from models import UserInDB as User
from models import UsernamePasswordForm, UserForm, UserUpdate
from auth import verify_password, get_password_hash
config = dotenv_values(".env")

app = FastAPI()

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")

# Select a database and collection
db = client["ieloro_users_db"]
users_collection = db["users"]


@app.post("/user", response_description="Create a new user", status_code=status.HTTP_201_CREATED) #, response_model=User)
async def create_user(request: Request, user: UserForm = Body(...)):
    
    user_obj = user.dict()

    # 
    user_obj.update({"account_info": {}})
    user_obj.update({"username": user_obj['email'].split("@")[0]})
    user_obj.update({"password": get_password_hash(user_obj['password'])})
    user_obj.update({"created_at": datetime.datetime.now().timestamp()})
    user_obj.update({"account_type_id": "USER"})
    user_obj.update({"is_super_admin": False})
    user_obj.update({"status": True})
    user_obj.update({"email_verified": False})
    user_obj.update({"phone_verified": False})
    # user_obj.pop("_id")
    

    try:
        print(users_collection.insert_one(user_obj)) #, bypass_document_validation=False, session=None, comment=None)
        # print(request.app.database["users"].insert_one(user_obj))
    except Exception as e:
        print(e)
        raise Exception(e)

    # created_user = request.app.database["users"].find_one({
    #     "_id": new_user.inserted_id
    # })

    return "new_user"


# app.include_router(user_router, tags=["users"], prefix="/user")