"""
event_db.py
By: Zack Bamford

Functions to modify and create events within the database
"""
from datetime import datetime
from typing import Optional

import sqlalchemy
from sqlalchemy.orm import Session, relationship
from sqlalchemy.orm import Mapped

from api.src.main.db import generic_db
from api.src.main.db.plan_db import PlanCommands, Plan
from api.src.main.db.user_db import User


class Event(generic_db.Base):
    """
    SQLAlchemy Class for event object
    """

    __tablename__ = "events"

    ID: Mapped[str] = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    name: Mapped[str] = sqlalchemy.Column(sqlalchemy.String)
    date: Mapped[datetime] = sqlalchemy.Column(sqlalchemy.DateTime)
    distance: Mapped[float] = sqlalchemy.Column(sqlalchemy.Float)
    distance_unit: Mapped[str] = sqlalchemy.Column(sqlalchemy.String)

    plan: Mapped["Plan"] = relationship(back_populates="child_events")

    def __repr__(self):
        return f"Event: {self.ID} {self.name} {self.date} {self.distance} {self.distance_unit}"

    def __eq__(self, other):
        # check if other is an event
        if not isinstance(other, Event):
            return False

        # check if all are equal
        return self.ID == other.ID and self.name == other.name and self.date == other.date and \
            self.distance == other.distance and self.distance_unit == other.distance_unit


class EventCommands:
    """
    Class to manage events within the database
    """

    def __init__(self, db_obj: generic_db.DBModificationObject):
        """
        Create a new EventCommands object

        :param db_obj: DBModificationObject to use
        """

        # add to db
        Event.metadata.create_all(db_obj.engine)

        self.engine: sqlalchemy.Engine = db_obj.engine

        self.pc: PlanCommands = PlanCommands(db_obj)

    def add_event(self, name: str, date: datetime, distance: float, distance_unit: str, plan_id: str) -> \
            Optional[Event]:
        """
        Add an event to the database

        :param name: Event name
        :param date: Event due date
        :param distance: Distance of event
        :param distance_unit: Distance unit of event
        :param plan_id: Plan ID to add event to
        :return: Created event
        """

    def retrieve_event(self, event_id: str) -> Optional[Event]:
        """
        Retrieve an event from the database

        :param event_id: Event ID to retrieve
        :return: Retrieved event
        """

    def modify_event(self, event_id: str, name: str, date: datetime, distance: float, distance_unit: str) -> \
            Optional[Event]:
        """
        Modify an event in the database

        :param event_id: Event ID to modify
        :param name: New event name
        :param date: New event due date
        :param distance: New event distance
        :param distance_unit: New event distance unit
        :return: Modified event
        """

    def delete_event(self, event_id: str) -> bool:
        """
        Delete an event from the database

        :param event_id: Event ID to delete
        :return: If the event was deleted
        """
