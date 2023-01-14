from fastapi import APIRouter, Depends, status, Response, HTTPException, Request
import json

from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from bson.json_util import dumps, loads

import datetime


router = APIRouter()

CACHE_KEY_PREFIX = "user:"


@router.put("/follow/@{username}")
def follow_user(request: Request, username: str):

    # user_id = request.app.current_user
    user_id = "5f9f1b0b0b9b9b0b9b0b9b0b" # current user id provided by jwt

    result = request.app.database["users"].update_many({"_id": user_id}, {"$push": {"following_users": username}}) # add current user to following_users list of user with username
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found")


@router.put("/unfollow/@{username}")
def follow_user(request: Request, username: str):
     # user_id = request.app.current_user
    user_id = "5f9f1b0b0b9b9b0b9b0b9b0b" # current user id provided by jwt

    result = request.app.database["users"].update_many({"_id": user_id}, {"$push": {"following_users": username}}) # add current user to following_users list of user with username
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found")


    cache_key = CACHE_KEY_PREFIX + user_id
    request.app.redis_client.set(cache_key, json.dumps(user_id))