"""
models.py
By: Zack Bamford

Pydantic models
"""

from typing import Annotated

from pydantic import BaseModel, EmailStr
from pydantic.fields import Field


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(min_length=12, max_length=72)


class User(UserBase):
    ID: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class EventBase(BaseModel):
    name: str
    description: str
    start_time: str
    end_time: str
    location: str
    plan_id: str


class EventCreate(EventBase):
    plan_id: str


class Event(EventBase):
    ID: str

    class Config:
        orm_mode = True


class RunBase(BaseModel):
    date: str
    status: str


class RunCreate(RunBase):
    event_id: str


class Run(RunBase):
    ID: str

    class Config:
        orm_mode = True
