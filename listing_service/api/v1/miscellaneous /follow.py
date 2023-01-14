from fastapi import APIRouter, Depends, status, Response, HTTPException, Request
import json

from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from bson.json_util import dumps, loads

import datetime


router = APIRouter()


@router.put("/follow/{listing_id}")
def follow_user(request: Request, listing_id: str):

    # user_id = request.app.current_user
    user_id = "5f9f1b0b0b9b9b0b9b0b9b0b" # current user id provided by jwt

    result = request.app.database["users"].update_many({"_id": user_id}, {"$push": {"following_listings": listing_id}}) 
    return result


@router.put("/unfollow/{listing_id}")
def follow_user(request: Request, listing_id: str):
     # user_id = request.app.current_user
    user_id = "5f9f1b0b0b9b9b0b9b0b9b0b" # current user id provided by jwt

    result = request.app.database["users"].update_many({"_id": user_id}, {"$pull": {"following_listings": listing_id}})
    return result

