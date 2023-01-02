from fastapi import FastAPI, status, Request, Response, Body

from conf import settings
from core import route

from datastructures.users import (UsernamePasswordForm,
                                  UserForm,
                                  UserUpdateForm)
from datastructures.listings import ListingForm

app = FastAPI()


@route(
    request_method=app.post,
    path='/api/login',
    status_code=status.HTTP_201_CREATED,
    payload_key='username_password',
    service_url=settings.USERS_SERVICE_URL,
    authentication_required=False,
    post_processing_func='post_processing.access_token_generate_handler',
    response_model='datastructures.users.LoginResponse'
)
async def login(username_password: UsernamePasswordForm,
                request: Request, response: Response):
    pass

'''

USER SERVICE

'''

@route(request_method=app.post,
    path='/user',
    status_code=status.HTTP_201_CREATED,
    payload_key='username_password',
    service_url=settings.USERS_SERVICE_URL,
    authentication_required=False,
    post_processing_func='post_processing.access_token_generate_handler',
    response_model='datastructures.users.LoginResponse')
def create_user(request: Request, user: UserForm = Body(...)):
    pass



# @router.get("/", response_description="List all users", response_model=List[User])
# def list_users(request: Request):
#     users = list(request.app.database["users"].find(limit=100))
#     return users


# @router.get("/{id}", response_description="Get a single user by id", response_model=User)
# def find_user(id: str, request: Request):
#     if (user := request.app.database["users"].find_one({"_id": id})) is not None:
#         return user

#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {id} not found")



# @route(
#     request_method=app.post,
#     path='/api/users',
#     status_code=status.HTTP_201_CREATED,
#     payload_key='user',
#     service_url=settings.USERS_SERVICE_URL,
#     authentication_required=True,
#     post_processing_func=None,
#     authentication_token_decoder='auth.decode_access_token',
#     service_authorization_checker='auth.is_admin_user',
#     service_header_generator='auth.generate_request_header',
#     response_model='datastructures.users.UserResponse',
# )
# async def create_user(user: UserForm, request: Request, response: Response):
#     pass


# @route(
#     request_method=app.get,
#     path='/api/users',
#     status_code=status.HTTP_200_OK,
#     payload_key=None,
#     service_url=settings.USERS_SERVICE_URL,
#     authentication_required=True,
#     post_processing_func=None,
#     authentication_token_decoder='auth.decode_access_token',
#     service_authorization_checker='auth.is_admin_user',
#     service_header_generator='auth.generate_request_header',
#     response_model='datastructures.users.UserResponse',
#     response_list=True
# )
# async def get_users(request: Request, response: Response):
#     pass


# @route(
#     request_method=app.get,
#     path='/api/users/{user_id}',
#     status_code=status.HTTP_200_OK,
#     payload_key=None,
#     service_url=settings.USERS_SERVICE_URL,
#     authentication_required=True,
#     post_processing_func=None,
#     authentication_token_decoder='auth.decode_access_token',
#     service_authorization_checker='auth.is_admin_user',
#     service_header_generator='auth.generate_request_header',
#     response_model='datastructures.users.UserResponse',
# )
# async def get_user(user_id: int, request: Request, response: Response):
#     pass


# @route(
#     request_method=app.delete,
#     path='/api/users/{user_id}',
#     status_code=status.HTTP_204_NO_CONTENT,
#     payload_key=None,
#     service_url=settings.USERS_SERVICE_URL,
#     authentication_required=True,
#     post_processing_func=None,
#     authentication_token_decoder='auth.decode_access_token',
#     service_authorization_checker='auth.is_admin_user',
#     service_header_generator='auth.generate_request_header',
# )
# async def delete_user(user_id: int, request: Request, response: Response):
#     pass


# @route(
#     request_method=app.put,
#     path='/api/users/{user_id}',
#     status_code=status.HTTP_200_OK,
#     payload_key='user',
#     service_url=settings.USERS_SERVICE_URL,
#     authentication_required=True,
#     post_processing_func=None,
#     authentication_token_decoder='auth.decode_access_token',
#     service_authorization_checker='auth.is_admin_user',
#     service_header_generator='auth.generate_request_header',
#     response_model='datastructures.users.UserResponse',
# )
# async def update_user(user_id: int, user: UserUpdateForm,
#                       request: Request, response: Response):
#     pass


# @route(
#     request_method=app.get,
#     path='/api/listings',
#     status_code=status.HTTP_200_OK,
#     payload_key=None,
#     service_url=settings.ORDERS_SERVICE_URL,
#     authentication_required=True,
#     post_processing_func=None,
#     authentication_token_decoder='auth.decode_access_token',
#     service_authorization_checker='auth.is_default_user',
#     service_header_generator='auth.generate_request_header',
#     response_model='datastructures.listings.OrderResponse',
#     response_list=True,
# )
# async def get_listings(request: Request, response: Response):
#     pass


# @route(
#     request_method=app.post,
#     path='/api/listings',
#     status_code=status.HTTP_200_OK,
#     payload_key='listing',
#     service_url=settings.ORDERS_SERVICE_URL,
#     authentication_required=True,
#     post_processing_func=None,
#     authentication_token_decoder='auth.decode_access_token',
#     service_authorization_checker='auth.is_default_user',
#     service_header_generator='auth.generate_request_header',
#     response_model='datastructures.listings.OrderResponse',
# )
# async def create_listing(listing: ListingForm, request: Request, response: Response):
#     pass
