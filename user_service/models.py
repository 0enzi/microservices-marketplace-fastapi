import uuid
from odmantic import EmbeddedModel, Model
from pydantic import BaseModel


class AccountType(Model):
    account_type_name: str
    permissions: list
    open_for_registration: bool
    status: bool

    class Config:
        collection = "accountTypes"


class UsernamePasswordForm(BaseModel):
    email: str 
    password: str


class UserForm(UsernamePasswordForm): 
    phone: str 
    location: str 
    

class UserInDB(Model):
    account_info: dict
    username: str
    email: str
    hashed_password: str
    phone: str 
    location: str
    created_at: str
    account_type_id: str
    is_super_admin: bool
    status: bool
    email_verified: bool
    phone_verified: bool


    class Config:
        collection = "users"

 
class UserUpdate(Model):
    name: str 
    email: str 
    phone: str 
    email_verified: bool 
    phone_verified: bool 
    location: str 
    account_type: str 
    status: bool 

    class Config:
        collection = "users"


    