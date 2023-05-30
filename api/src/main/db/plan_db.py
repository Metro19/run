"""
plan_db.py
By: Zack Bamford

Functions to modify and create plans within the database
"""

import logging
from datetime import datetime
from typing import Optional, Union, List

import sqlalchemy
from sqlalchemy.ext.hybrid import hybrid_method
from sqlalchemy.orm import Session, relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.elements import and_

from api.src.main.db import generic_db
from api.src.main.db.user_db import User


def sep_users(users: str) -> list[str]:
    """
    Separate users string into a list of users

    :param users: Users string
    :return: List of users
    """

    # empty string, empty list
    if users == "":
        return []

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

    # relationship with child event
    plan_members: Mapped[List["PlanMember"]] = relationship(cascade="all, delete-orphan",
                                                            primaryjoin="Plan.ID == PlanMember.plan_id")
    child_events: Mapped[List["Event"]] = relationship(back_populates="plan", cascade="all, delete-orphan")

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



class Event(generic_db.Base):
    """
    SQLAlchemy Class for event object
    """

    __tablename__ = "events"

    ID: Mapped[str] = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    plan_id: Mapped[str] = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("plans.ID"))
    name: Mapped[str] = sqlalchemy.Column(sqlalchemy.String)
    date: Mapped[datetime] = sqlalchemy.Column(sqlalchemy.DateTime)
    distance: Mapped[float] = sqlalchemy.Column(sqlalchemy.Float)
    distance_unit: Mapped[str] = sqlalchemy.Column(sqlalchemy.String)

    plan: Mapped["Plan"] = relationship(back_populates="child_events")
    run: Mapped[List["Run"]] = relationship("Run", cascade="all, delete-orphan")

    class Config:
        orm_mode = True

    def __hash__(self):
        return hash(self.ID)

    def __repr__(self):
        return f"Event: {self.ID} {self.name} {self.date} {self.distance} {self.distance_unit}"

    def __eq__(self, other):
        # check if other is an event
        if not isinstance(other, Event):
            return False

        # check if all are equal
        return self.ID == other.ID and self.name == other.name and self.date == other.date and \
            self.distance == other.distance and self.distance_unit == other.distance_unit

    def equals_no_id(self, other):
        """
        Check to see if two events are equal, but ignore the ID

        :param other: Other event object
        :return:
        """

        # check if other is an event
        if not isinstance(other, Event):
            return False

        # check if all are equal
        return self.name == other.name and self.date == other.date and self.distance == other.distance and \
            self.distance_unit == other.distance_unit


class Run(generic_db.Base):
    """
    SQLAlchemy Class for run object
    """

    __tablename__ = "runs"

    ID: Mapped[str] = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    event_id: Mapped[str] = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("events.ID"))
    usr_id: Mapped[str] = sqlalchemy.Column(sqlalchemy.String)
    date: Mapped[datetime] = sqlalchemy.Column(sqlalchemy.DateTime)
    status: Mapped[str] = sqlalchemy.Column(sqlalchemy.String)

    event: Mapped["Event"] = relationship("Event", back_populates="run")

    class Config:
        orm_mode = True

    def __hash__(self):
        return hash(self.ID)

    def __repr__(self):
        return f"Run: {self.ID} {self.usr_id} {self.date} {self.status}"

    def __eq__(self, other):
        # check if other is an event
        if not isinstance(other, Run):
            return False

        # check if all are equal
        return self.ID == other.ID and self.date == other.date and self.status == other.status

    def equals_no_id(self, other):
        """
        Check to see if two runs are equal, but ignore the ID

        :param other: Other run object
        :return: If the two runs are equal, but ignore the ID
        """

        # check if other is an event
        if not isinstance(other, Run):
            return False

        # check if all are equal
        return self.date == other.date and self.status == other.status


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

    def create_plan(self, name: str, description: str, date: datetime, distance: float, distance_unit: str) -> Optional[
        Plan]:
        """
        Create a new plan

        :param name: Name of the plan
        :param description: Description of the plan
        :param date: Date of the plan
        :param distance: Distance of the plan
        :param distance_unit: Distance unit of the plan
        :return: New plan object
        """

        # create new plan object
        new_plan = Plan(ID=generic_db.create_id("PLAN"), name=name, description=description, date=date,
                        distance=distance, distance_unit=distance_unit, users="")

        # add to db
        with Session(self.engine) as session:
            session.add(new_plan)
            session.commit()

            created_plan = session.get(Plan, new_plan.ID)

        logging.debug(f"Created plan: {created_plan}")

        return created_plan

    def retrieve_plan(self, plan_id: str) -> Optional[Plan]:
        """
        Get a plan by its ID

        :param plan_id: ID of the plan
        :return: Plan object
        """

        # get plan from db
        with Session(self.engine) as session:
            p: Optional[Plan] = session.get(Plan, plan_id)

            logging.debug(f"Retrieved plan: %s", p)
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

    def add_users_to_plan(self, plan_id: str, users: Union[list[User], list[str]]) -> Optional[Plan]:
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

        # get user list and add users if not empty
        user_list = []
        if p.users:
            user_list = sep_users(p.users)
        user_list += users

        # remove duplicates
        user_list = list(set(user_list))

        with Session(self.engine) as session:
            # get plan
            curr_plan = session.get(Plan, plan_id)

            # update plan with user list
            curr_plan.users = join_users(user_list)
            session.commit()

            return session.get(Plan, plan_id)

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

        with Session(self.engine) as session:
            # get plan
            curr_plan = session.get(Plan, plan_id)

            # update plan with user list
            curr_plan.users = join_users(user_list)
            session.commit()

            return session.get(Plan, plan_id)

    def modify_plan(self, plan_id: str, new_name: str, new_description: str, new_date: datetime, new_distance: float,
                    new_distance_unit: str) -> Optional[Plan]:
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
            p.description = new_description
            p.date = new_date
            p.distance = new_distance
            p.distance_unit = new_distance_unit

            session.commit()

            logging.debug(f"Modified plan: {p}")
            return session.get(Plan, plan_id)

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
