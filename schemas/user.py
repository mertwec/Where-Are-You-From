from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator


class UserBase(BaseModel):
    email: EmailStr


class InputUserData(UserBase):
    password: str = Field(min_length=4)
    password_repeat: str = Field(min_length=4)

    @model_validator(mode="after")
    @classmethod
    def valid_pass(cls, data: Any):
        if data.password != data.password_repeat:
            raise ValueError("passwords not match")
        return data


class UserData(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    create_date: datetime


class ListBaseUsers(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    users: list[UserData]
    count_users: int


class Token(BaseModel):
    access_token: str
    token_type: str
