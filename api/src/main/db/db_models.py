import enum
from datetime import datetime
from typing import List

import sqlalchemy as sqlalchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm.base import Mapped

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

    plan_members: Mapped[List["PlanMember"]] = sqlalchemy.orm.relationship(cascade="all, delete-orphan",
                                                                           primaryjoin="User.ID == PlanMember.user_id")

    class Config:
        orm_mode = True

    def __repr__(self):
        return f"User: {self.ID} {self.username} {self.email} {self.password}"

    def __eq__(self, other):
        # check for same type
        if not isinstance(other, User):
            return False

        return self.ID == other.ID and self.username == other.username and self.email == other.email and \
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


class Plan(generic_db.Base):
    """Datatable to manage a plan"""

    __tablename__ = "plans"

    ID: Mapped[str] = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    name: Mapped[str] = sqlalchemy.Column(sqlalchemy.String)
    description: Mapped[str] = sqlalchemy.Column(sqlalchemy.String)
    date: Mapped[datetime] = sqlalchemy.Column(sqlalchemy.DateTime)
    distance: Mapped[float] = sqlalchemy.Column(sqlalchemy.Float)
    distance_unit: Mapped[str] = sqlalchemy.Column(sqlalchemy.String)
    # users: Mapped[str] = sqlalchemy.Column(sqlalchemy.String)  # user ID separated by "#"

    # relationship with child event
    plan_members: Mapped[List["PlanMember"]] = relationship(cascade="all, delete-orphan",
                                                            primaryjoin="Plan.ID == PlanMember.plan_id")
    child_events: Mapped[List["Event"]] = relationship(back_populates="plan", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Plan: {self.ID} {self.name} {self.description} {self.date} {self.distance} {self.distance_unit}"

    def __eq__(self, other):
        # check for same type
        if not isinstance(other, Plan):
            return False

        return self.ID == other.ID and self.name == other.name and self.description == other.description and \
            self.date == other.date and self.distance == other.distance and self.distance_unit == other.distance_unit

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


class PlanPermissions(enum.Enum):
    """
    Enum for plan permissions
    """
    OWNER = 0
    ADMIN = 1
    PARTICIPANT = 2


class PlanMember(generic_db.Base):
    """
    SQLAlchemy PlanMember table model
    """

    __tablename__ = 'plan_member'

    ID: Mapped[str] = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    permission: Mapped[PlanPermissions] = sqlalchemy.Column(sqlalchemy.Enum(PlanPermissions))

    plan_id: Mapped[str] = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("plans.ID"))
    user_id: Mapped[str] = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("users.ID"))
