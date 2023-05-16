"""
auth.py
By: Zack Bamford

OAuth2 authentication functions
"""

import os
from datetime import timedelta, datetime
from typing import Annotated

import bcrypt
from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.params import Depends

from fastapi.security.oauth2 import OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import JWTError

from api.src.main.api.models import TokenData
from api.src.main.db import generic_db
from api.src.main.db.user_db import UserCommands

# db reader setup
uc: UserCommands = UserCommands(generic_db.db_obj)

# token setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
assert os.environ["SECRET_KEY"]
SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def authenticate_user(username: str, password: str):
    # get user
    user = uc.retrieve_user_by_email(username)

    # check for success
    if user is None:
        return False

    # check for valid password
    if not bcrypt.checkpw(password.encode('utf-8'), user.password):
        return False

    return True


def retrieve_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """
    Retrieves a user

    :param user_id: User_ID
    :param token: OAuth 2 token
    :return: User object
    """

    # credential check
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # try decoding token
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    retrieved_user = uc.retrieve_user(token_data.username)

    # check for success
    if retrieved_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return retrieved_user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    # set expiration
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    # complete encoding
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
