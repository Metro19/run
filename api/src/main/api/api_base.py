"""
api_base.py
By: Zack Bamford

This file contains the base API for the app.
"""
import os
from datetime import datetime, timedelta
from typing import Annotated
import bcrypt

from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import JWTError

from . import auth
from .auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from .models import TokenData
from .routers import user_api, plan_api, event_api, run_api
from ..db import generic_db
from ..db.user_db import UserCommands

app = FastAPI()

# docs metadata
tags_metadata = [
    {
        "name": "User",
        "description": "Operations with users."
    },
    {
        "name": "Plan",
        "description": "Operations with plans."
    }
]

# setup up sub files
app.router.include_router(user_api.router)
app.router.include_router(plan_api.router)
app.router.include_router(event_api.router)
app.router.include_router(run_api.router)

# setup user commands
uc: UserCommands = UserCommands(generic_db.db_obj)


@app.get("/ping", tags=["Default"])
async def test():
    return {"message": "Success!"}


@app.post("/token", tags=["Auth"])
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    # get user
    user = uc.retrieve_user_by_email(form_data.username)

    # check for success
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # verify password
    if not auth.authenticate_user(form_data.username, form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # create token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token({"sub": user.ID}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}
