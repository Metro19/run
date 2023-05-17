"""
user_api.py
By: Zack Bamford

User API operations
"""
from typing import Annotated

import bcrypt
from fastapi import HTTPException, APIRouter
from fastapi.params import Depends
from pydantic import EmailStr

from api.src.main.api import models
from api.src.main.api.auth import oauth2_scheme, retrieve_user
from api.src.main.db import generic_db
from api.src.main.db.user_db import UserCommands, User

router = APIRouter()

User.metadata.create_all(bind=generic_db.db_obj.engine)
uc: UserCommands = UserCommands(generic_db.db_obj)


@router.post("/user/create", tags=["User"])
def create_user(username: str, email: EmailStr, password: str):
    """
    Creates a user

    :param username: Username
    :param email: Email address
    :param password: Password
    :return: Created user object
    """

    # Check if email is already used
    user_check = uc.retrieve_user_by_email(email)

    if user_check is not None:
        raise HTTPException(status_code=409, detail="Email already in use")

    created_user = uc.create_user(username, email,
                                  bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(15)).decode('utf-8'))

    # check for success
    if created_user is None:
        raise HTTPException(status_code=500, detail="Failed to create user")

    return created_user


@router.get("/user/info", response_model=models.User, tags=["User"])
def get_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """
    Retrieves a user

    :param token: OAuth 2 token
    :return: User object
    """
    # get user
    user = retrieve_user(token)

    # check for success
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.post("/user/modify", response_model=models.User, tags=["User"])
def modify_user(token: Annotated[str, Depends(oauth2_scheme)],
                username: str | None = None, email: EmailStr | None = None, ):
    """
    Modify a user

    :param user_id: User ID to modify
    :param token: OAuth 2 token
    :param username: New name
    :param email: New email
    :return: Updated user
    """

    # get user
    retrieved_user = retrieve_user(token)

    # check for success
    if retrieved_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # overwrite optional fields
    if username is not None:
        retrieved_user.username = username

    if email is not None:
        retrieved_user.email = email

    # commit changes
    modified_user = uc.modify_user(retrieved_user.ID, retrieved_user.username, retrieved_user.email,
                                   retrieved_user.password)

    return modified_user


@router.delete("/user/delete", response_model=models.User, tags=["User"])
def delete_user(token: Annotated[str, Depends(oauth2_scheme)]):
    # get user
    retrieved_user = retrieve_user(token)

    # check for success
    if retrieved_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # delete user
    deleted = uc.delete_user(retrieved_user.ID)

    # see if operation succeeded
    if deleted is False:
        raise HTTPException(status_code=500, detail="Failed to delete user")
    else:
        raise HTTPException(status_code=200, detail="User deleted")
