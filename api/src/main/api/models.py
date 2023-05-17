"""
models.py
By: Zack Bamford

Pydantic models
"""
from datetime import datetime
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
    date: datetime
    distance: str
    distance_unit: str


class EventCreate(EventBase):
    plan_id: str


class Event(EventBase):
    ID: str

    class Config:
        orm_mode = True


class RunBase(BaseModel):
    date: datetime
    status: str


class RunCreate(RunBase):
    usr_id: str
    event_id: str


class Run(RunBase):
    ID: str

    class Config:
        orm_mode = True
