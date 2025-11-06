from pydantic import BaseModel, Field
from typing import Optional
import uuid
from datetime import datetime


class UserModel(BaseModel):
    uid: uuid.UUID
    username: str
    fullname: Optional[str] = None
    is_verified: bool
    email: str
    hashed_password: str = Field(exclude=True)
    role: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserCreateModel(BaseModel):
    username: str
    fullname: Optional[str] = None
    email: str
    hashed_password: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "Username",
                "fullname": "Fullname",
                "email": "User_1@gmail.com",
                "password": "********",
            }
        }
    }


class UserLoginModel(BaseModel):
    identifier: str
    password: str


class UserUpdateModel(BaseModel):
    username: Optional[str] = None
    fullname: Optional[str] = None
    email: Optional[str] = None
    hashed_password: Optional[str] = None


class AdminUpdateModel(UserUpdateModel):
    role: Optional[str] = None
