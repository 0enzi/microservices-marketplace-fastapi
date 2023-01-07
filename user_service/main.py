from fastapi import FastAPI, APIRouter, Body, Request, Response, HTTPException, status
from dotenv import dotenv_values
from pymongo import MongoClient
from api.v1 import api_router as user_routes
import redis


import datetime
from models import UserInDB as User
from models import UsernamePasswordForm, UserForm, UserUpdate
# from usauth import verify_password, get_password_hash
config = dotenv_values(".env")

app = FastAPI()
app.include_router(user_routes, prefix="/api/v1")

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")

# Select a database and collection
db = client["ieloro_users_db"]
users_collection = db["users"]

@app.on_event("startup")
async def startup():
    # Connect to MongoDB
    app.mongo_client = MongoClient("mongodb+srv://dev:Admin1234@ieoloro-cluster1.g7vtwdw.mongodb.net/?retryWrites=true&w=majority", tls=True, tlsAllowInvalidCertificates=True)
    app.database = app.mongo_client["ieloro_users_db"]

    # Connect to Redis
    app.redis_client = redis.Redis(host='docker.for.mac.localhost', port=6379)

    print("Connected to MongoDB and Redis", app.database, app.redis_client)
 




# app.include_router(user_router, tags=["users"], prefix="/user")