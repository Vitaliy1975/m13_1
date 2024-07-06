from datetime import date,datetime
from pydantic import BaseModel, Field,EmailStr


class ContactModel(BaseModel):
    first_name:str=Field(min_length=2,max_length=25)
    last_name:str=Field(min_length=2,max_length=25)
    email:EmailStr
    phone_number:int=Field()
    birthday:date
    additional_data:str=Field(max_length=255)
    user_id:int=Field(default=None)

    class Config:
        orm_mode=True


class ContactResponse(BaseModel):
    id:int
    first_name:str
    last_name:str
    email:EmailStr
    phone_number:int
    birthday:date
    additional_data:str
    user_id:int

    class Config:
        orm_mode=True


class UserModel(BaseModel):
    username: str = Field(min_length=2, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    avatar: str

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    email: EmailStr
