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
from api.src.main.db.plan_db import PlanCommands, Plan, Run
from api.src.main.db.user_db import User
from api.src.main.db.plan_db import Event


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

        with Session(self.engine) as session:
            # check for valid plan
            plan: Optional[Plan] = session.get(Plan, plan_id)

            if plan is None:
                return None

            # create event
            event: Event = Event(ID=generic_db.create_id("EVENT"), name=name, date=date, distance=distance,
                                 distance_unit=distance_unit)

            # add to db
            plan.child_events.append(event)

            session.commit()

            return session.get(Event, event.ID)

    def retrieve_event(self, event_id: str) -> Optional[Event]:
        """
        Retrieve an event from the database

        :param event_id: Event ID to retrieve
        :return: Retrieved event
        """

        with Session(self.engine) as session:
            return session.get(Event, event_id)

    def get_all_run_ids(self, event_id: str) -> Optional[list[Run]]:
        """
        Get all event IDs

        :param event_id: Event ID to get all run IDs for
        :return: List of event IDs, or none if error
        """

        with Session(self.engine) as session:
            # check for valid event
            event: Optional[Event] = session.get(Event, event_id)

            if event is None:
                return []

            return event.run


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

        with Session(self.engine) as session:
            # check for valid event
            event: Optional[Event] = session.get(Event, event_id)

            if event is None:
                return None

            # modify event
            event.name = name
            event.date = date
            event.distance = distance
            event.distance_unit = distance_unit

            session.commit()

            return session.get(Event, event.ID)

    def delete_event(self, event_id: str) -> bool:
        """
        Delete an event from the database

        :param event_id: Event ID to delete
        :return: If the event was deleted
        """

        with Session(self.engine) as session:
            # check for valid event
            event: Optional[Event] = session.get(Event, event_id)

            if event is None:
                return False

            # delete event
            session.delete(event)

            session.commit()

            return True