from fastapi import FastAPI, APIRouter, Body, Request, Response, HTTPException, status
from dotenv import dotenv_values
from pymongo import MongoClient
from api.v1 import api_router as user_routes
import redis, datetime

config = dotenv_values(".env")

app = FastAPI()
app.include_router(user_routes, prefix="/api/v1")



@app.on_event("startup")
async def startup():
    # Connect to MongoDB
    app.mongo_client = MongoClient(config['MONGODB_URI'], tls=True, tlsAllowInvalidCertificates=True)
    app.database = app.mongo_client["ieloro_users_db"]

    # Connect to Redis
    app.redis_client = redis.Redis(host='docker.for.mac.localhost', port=6379)

    print("Connected to MongoDB and Redis", app.database, app.redis_client)
 




# app.include_router(user_router, tags=["users"], prefix="/user")