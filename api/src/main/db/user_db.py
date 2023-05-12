"""
user_db.py
By: Zack Bamford

Functions to modify and create users within the database
"""
import logging
from typing import Optional

import sqlalchemy
from sqlalchemy.orm import Session

from api.src.main.db import generic_db


class User(generic_db.Base):
    """
    Datatable to manage a user
    """

    ID: str
    username: str
    email: str
    password: str

    def __str__(self):
        return f"User: {self.ID} {self.username} {self.email} {self.password}"


class UserCommands:
    """Database commands for a user object"""

    def __init__(self, db_obj: generic_db.DBModificationObject):
        """
        Create a new UserCommands object

        :param db_obj: DBModificationObject to use
        """
        self.engine: sqlalchemy.Engine = db_obj.engine

    def create_user(self, name: str, email: str, password: str) -> Optional[User]:
        """
        Create a new user

        :param name: Name of the user
        :param email: Email of the user
        :param password: Password of the user
        :return: User object or none if error
        """

        user = User(ID=generic_db.create_id("USER"), username=name, email=email, password=password)

        # add to session and commit
        with Session(self.engine) as session:
            session.add(user)
            session.commit()

        logging.debug("Created user: %s", user)

        return user

    def retrieve_user(self, user_id: str) -> Optional[User]:
        """
        Retrieve a user object from the database

        :param user_id: Existing user id
        :return: User object or None if error
        """

        with Session(self.engine) as session:
            u: Optional[User] = session.get(User, user_id)

            logging.debug("Retrieved user: %s", u)
            return u

    def modify_user(self, user_id: str, new_username: str, new_email: str, new_password: str) -> Optional[User]:
        """
        Modify an existing user object

        :param user_id: Existing User ID
        :param new_username: New username
        :param new_email: New email
        :param new_password: New password
        :return: New user if successful, or None if error
        """

        # try and get user object
        with Session(self.engine) as session:
            u: Optional[User] = session.get(User, user_id)

            # check if user does exist
            if u is None:
                return None

            # write information
            u.username = new_username
            u.email = new_email
            u.password = new_password

            logging.debug("Modified user: %s", u)

            # commit
            session.commit()

    def delete_user(self, user_id: str) -> bool:
        """
        Delete a user from the database

        :param user_id: User ID to delete
        :return: T/F on success
        """

        with Session(self.engine) as session:
            # get object
            u: Optional[User] = session.get(User, user_id)

            # check if object exists
            if u is None:
                return False

            logging.debug("Deleted user: %s", u)

            # delete object
            session.delete(u)
