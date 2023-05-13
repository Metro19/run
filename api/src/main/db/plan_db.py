"""
plan_db.py
By: Zack Bamford

Functions to modify and create plans within the database
"""

import logging
from datetime import datetime
from typing import Optional, Union

import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy.orm import Mapped

from api.src.main.db import generic_db
from api.src.main.db.user_db import User


def sep_users(users: str) -> list[str]:
    """
    Separate users string into a list of users

    :param users: Users string
    :return: List of users
    """

    return users.split("#")


def join_users(users: list[str]) -> str:
    """
    Join a list of users into a string

    :param users: List of users
    :return: Users string
    """

    return "#".join(users)


class Plan(generic_db.Base):
    """Datatable to manage a plan"""

    __tablename__ = "plans"

    ID: Mapped[str] = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    name: Mapped[str] = sqlalchemy.Column(sqlalchemy.String)
    description: Mapped[str] = sqlalchemy.Column(sqlalchemy.String)
    date: Mapped[datetime] = sqlalchemy.Column(sqlalchemy.DateTime)
    distance: Mapped[float] = sqlalchemy.Column(sqlalchemy.Float)
    distance_unit: Mapped[str] = sqlalchemy.Column(sqlalchemy.String)
    users: Mapped[str] = sqlalchemy.Column(sqlalchemy.String)  # user ID separated by "#"

    def __repr__(self):
        return f"Plan: {self.ID} {self.name} {self.description} {self.date} {self.distance} {self.distance_unit} " \
               f"{sep_users(self.users)}"

    def __eq__(self, other):
        # check for same type
        if not isinstance(other, Plan):
            return False

        return self.ID == other.ID and self.name == other.name and self.description == other.description and \
            self.date == other.date and self.distance == other.distance and self.distance_unit == other.distance_unit \
            and self.users == other.users

    def equals_no_id(self, other):
        """
        Check to see if two plans are equal, but ignore the ID

        :param other: Other plan object
        :return: If the two plans are equal, but ignore the ID
        """

        # check for same type
        if not isinstance(other, Plan):
            return False

        return self.name == other.name and self.description == other.description and self.date == other.date and \
            self.distance == other.distance and self.distance_unit == other.distance_unit


class PlanCommands:
    """Database commands for a plan object"""

    def __init__(self, db_obj: generic_db.DBModificationObject):
        """
        Create a new PlanCommands object

        :param db_obj: DBModificationObject to use
        """

        # add to db
        Plan.metadata.create_all(db_obj.engine)

        self.engine: sqlalchemy.Engine = db_obj.engine

    def create_plan(self, name: str, date: datetime, distance: float, distance_unit: str) -> Optional[Plan]:
        """
        Create a new plan

        :param name: Name of the plan
        :param date: Date of the plan
        :param distance: Distance of the plan
        :param distance_unit: Distance unit of the plan
        :return: New plan object
        """

        # create new plan object
        new_plan = Plan(ID=generic_db.create_id("PLAN_"), name=name, date=date, distance=distance,
                        distance_unit=distance_unit, users="")

        # add to db
        with Session(self.engine) as session:
            session.add(new_plan)
            session.commit()

        logging.debug(f"Created plan: {new_plan}")

        return new_plan

    def retrieve_plan(self, plan_id: str) -> Optional[Plan]:
        """
        Get a plan by its ID

        :param plan_id: ID of the plan
        :return: Plan object
        """

        # get plan from db
        with Session(self.engine) as session:
            p: Optional[Plan] = session.get(Plan, plan_id)

        logging.debug(f"Retrieved plan: {p}")
        return p

    def get_user_ids_in_plan(self, plan_id: str) -> Optional[list[str]]:
        """
        Get the user IDs in a plan

        :param plan_id: Plan ID to retrieve from
        :return: List of user IDs, or None if the plan does not exist
        """

        p: Optional[Plan] = self.retrieve_plan(plan_id)

        # check for no response
        if p is None:
            return None

        # return the ids
        return sep_users(p.users)

    def get_user_objects_in_plan(self, plan_id: str) -> Optional[list[User]]:
        """
        Get the user objects in the plan

        :param plan_id: Plan ID to get users from
        :return: Users in the plan
        """

        p: Optional[Plan] = self.retrieve_plan(plan_id)

        # check for no response
        if p is None:
            return None

        users = []

        with Session(self.engine) as session:

            # get all users
            for user_id in sep_users(p.users):
                curr_user: Optional[User] = session.get(User, user_id)

                # verify user
                if curr_user is not None:
                    users.append(curr_user)

        logging.debug(f"Retrieved users in plan: {users}")
        return users

    def add_users_from_plan(self, plan_id: str, users: Union[list[User], list[str]]) -> Optional[Plan]:
        """
        Add users to a plan

        :param plan_id: Plan ID to modify
        :param users: Users to add, or user IDs to add
        :return: Plan with users added
        """

        p: Optional[Plan] = self.retrieve_plan(plan_id)

        # check for no response
        if p is None:
            return None

        # format as list of user ids
        if type(users[0]) == User:
            users = [user.ID for user in users]

        # get user list and add users
        user_list = sep_users(p.users)
        user_list += users

        # remove duplicates
        user_list = list(set(user_list))

        # update plan
        self.modify_plan(plan_id, p.name, p.date, p.distance, p.distance_unit, join_users(user_list))

    def remove_users_from_plan(self, plan_id: str, users: Union[list[User], list[str]]) -> Optional[Plan]:
        """
        Remove users from a plan

        :param plan_id: Plan ID to modify
        :param users: Users to remove, or user IDs to remove
        :return: Plan with users removed
        """

        p: Optional[Plan] = self.retrieve_plan(plan_id)

        # check for no response
        if p is None:
            return None

        # format as list of user ids
        if type(users[0]) == User:
            users = [user.ID for user in users]

        # get user list and remove users with list comprehension
        user_list = sep_users(p.users)
        user_list = [user for user in user_list if user not in users]

        # update plan
        self.modify_plan(plan_id, p.name, p.date, p.distance, p.distance_unit, join_users(user_list))

    def modify_plan(self, plan_id: str, new_name: str, new_date: datetime, new_distance: float,
                    new_distance_unit: str, new_user_list: str) -> Optional[Plan]:
        """
        Modify a plan

        :param new_user_list:
        :param plan_id: ID of the plan
        :param new_name: New name of the plan
        :param new_date: New date of the plan
        :param new_distance: New distance of the plan
        :param new_distance_unit: New distance unit of the plan
        :param new_user_list: New user list of the plan
        :return: Modified plan object
        """

        # get plan from db
        with Session(self.engine) as session:
            p: Optional[Plan] = session.get(Plan, plan_id)

            if p is None:
                logging.debug(f"Could not find plan with ID {plan_id}")
                return None

            # modify plan
            p.name = new_name
            p.date = new_date
            p.distance = new_distance
            p.distance_unit = new_distance_unit
            p.users = new_user_list

            session.commit()

        logging.debug(f"Modified plan: {p}")
        return p

    def delete_plan(self, plan_id: str) -> bool:
        """
        Delete a plan

        :param plan_id: ID of the plan
        :return: If the plan was deleted
        """

        # get plan from db
        with Session(self.engine) as session:
            p: Optional[Plan] = session.get(Plan, plan_id)

            if p is None:
                logging.debug(f"Could not find plan with ID {plan_id}")
                return False

            # delete plan
            session.delete(p)
            session.commit()

        logging.debug(f"Deleted plan: {p}")
        return True
