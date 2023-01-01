
from pydantic import BaseModel, EmbeddedModel


class AccountType(BaseModel):
    account_type_name:str
    permissions: list
    open_for_registration: bool
    status: bool


class UsernamePasswordForm(BaseModel):
    username: str
    password: str


class UserForm(UsernamePasswordForm):
    email: str = None
    full_name: str = None
    user_type: str
    location: str
    account_type: EmbeddedModel[AccountType]


class UserUpdateForm(BaseModel):
    username: str = None
    email: str = None
    full_name: str = None
    user_type: str = None
    location: str = None


class UserInDb(BaseModel):
    full_name: str = None
    username: str
    email: str = None
    hashed_password: str
    phone: str = None
    location: str = None
    created_at: str
    account_type: EmbeddedModel[AccountType]
    is_super_admin: bool
    status: bool
    email_verified: bool
    phone_verified: bool
