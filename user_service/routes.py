from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
import datetime
from models import UserInDB as User
from models import UsernamePasswordForm, UserForm, UserUpdate
from auth import verify_password, get_password_hash


router = APIRouter()


@router.post('/api/login', status_code=status.HTTP_201_CREATED)
async def login(request: Request, form_data: UsernamePasswordForm):
    user_in_db = request.app.database["users"].find_one({"email": form_data.email})

    if not user_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found with this email.',
        )

    # verified = verify_password(form_data.password, user_in_db.hashed_password)
    # if not verified:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail='Password is wrong.',
    #     )

    return True
    # retu
    # rn user_in_db

@router.post("/", response_description="Create a new user", status_code=status.HTTP_201_CREATED) #, response_model=User)
def create_user(request: Request, user: UserForm = Body(...)):
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
        print(request.app.database["users"].insert_one(user_obj))
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")

    # created_user = request.app.database["users"].find_one({
    #     "_id": new_user.inserted_id
    # })

    return "new_user"



@router.get("/", response_description="List all users", response_model=List[User])
def list_users(request: Request):
    users = list(request.app.database["users"].find(limit=100))
    return users


@router.get("/{id}", response_description="Get a single user by id", response_model=User)
def find_user(id: str, request: Request):
    if (user := request.app.database["users"].find_one({"_id": id})) is not None:
        return user

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {id} not found")


# @router.put("/{id}", response_description="Update a user", response_model=User)
# def update_user(id: str, request: Request, user: UserUpdate = Body(...)):
#     user = {k: v for k, v in user.dict().items() if v is not None}

#     if len(user) >= 1:
#         update_result = request.app.database["users"].update_one(
#             {"_id": id}, {"$set": user}
#         )

#         if update_result.modified_count == 0:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {id} not found")

#     if (
#         existing_user := request.app.database["users"].find_one({"_id": id})
#     ) is not None:
#         return existing_user

#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {id} not found")


@router.delete("/{id}", response_description="Delete a user")
def delete_user(id: str, request: Request, response: Response):
    delete_result = request.app.database["users"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {id} not found")