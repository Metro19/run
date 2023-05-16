"""
user_db.py
By: Zack Bamford

Functions to modify and create users within the database
"""
import logging
from typing import Optional

import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy.orm import Mapped

from api.src.main.db import generic_db


class User(generic_db.Base):
    """
    Datatable to manage a user
    """

    __tablename__ = "users"

    ID: Mapped[str] = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    username: Mapped[str] = sqlalchemy.Column(sqlalchemy.String)
    email: Mapped[str] = sqlalchemy.Column(sqlalchemy.String)
    password: Mapped[str] = sqlalchemy.Column(sqlalchemy.String)

    class Config:
        orm_mode = True

    def __repr__(self):
        return f"User: {self.ID} {self.username} {self.email} {self.password}"

    def __eq__(self, other):
        # check for same type
        if not isinstance(other, User):
            return False

        return self.ID == other.ID and self.username == other.username and self.email == other.email and\
            self.password == other.password

    def equals_no_id(self, other):
        """
        Check to see if two users are equal, but ignore the ID

        :param other: Other user object
        :return: If the two users are equal, but ignore the ID
        """
        # check for same type
        if not isinstance(other, User):
            return False

        return self.username == other.username and self.email == other.email and self.password == other.password


class UserCommands:
    """Database commands for a user object"""

    def __init__(self, db_obj: generic_db.DBModificationObject):
        """
        Create a new UserCommands object

        :param db_obj: DBModificationObject to use
        """
        # add to db
        User.metadata.create_all(db_obj.engine)

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

            created_user = session.get(User, user.ID)

        logging.debug("Created user: %s", user)

        return created_user

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

            # return updated user object
            return session.get(User, user_id)

    def retrieve_user_by_email(self, email: str) -> Optional[User]:
        """
        Retrieve a user by their email

        :param email: Email to retrieve by
        :return: User if found, or none
        """

        with Session(self.engine) as session:
            # get user
            u: Optional[User] = session.query(User).filter(User.email == email).first()

            logging.debug("Retrieved user by email: %s", u)
            return u

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

            return True