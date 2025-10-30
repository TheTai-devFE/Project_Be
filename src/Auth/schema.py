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
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserCreateModel(BaseModel):
    username: str
    fullname: Optional[str] = None
    email: str
    password: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "User1",
                "fullname": "User Fullname",
                "email": "User_1@gmail.com",
                "password": "strongpassword123",
            }
        }
    }


class UserLoginModel(BaseModel):
    identifier: str
    password: str
