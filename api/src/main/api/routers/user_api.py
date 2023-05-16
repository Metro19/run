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

# setup
router = APIRouter()
User.metadata.create_all(bind=generic_db.db_obj.engine)
uc: UserCommands = UserCommands(generic_db.db_obj)


@router.post("/user", response_model=models.User)
def create_user(user: models.UserCreate):
    """
    Creates a user
    """
    # TODO: Check if email is already used
    created_user = uc.create_user(user.username, user.email,
                                  bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt(15)))

    # check for success
    if created_user is None:
        raise HTTPException(status_code=500, detail="Failed to create user")

    return created_user


# @router.get("/user/{user_id}", response_model=models.User)

@router.get("/get_user_information", response_model=models.User)
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


@router.post("/user/modify", response_model=models.User)
def modify_user(user_id: str, username: str | None = None, email: EmailStr | None = None):
    """
    Modify a user

    :param user_id: User ID to modify
    :param username: New name
    :param email: New email
    :return: Updated user
    """

    # get user
    retrieved_user = uc.retrieve_user(user_id)

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
