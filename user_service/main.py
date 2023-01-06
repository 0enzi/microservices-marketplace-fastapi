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
app.include_router(api_router, prefix=settings.API_V1_STR)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")

# Select a database and collection
db = client["ieloro_users_db"]
users_collection = db["users"]






# app.include_router(user_router, tags=["users"], prefix="/user")