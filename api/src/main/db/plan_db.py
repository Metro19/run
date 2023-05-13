"""
plan_db.py
By: Zack Bamford

Functions to modify and create plans within the database
"""

import logging
from datetime import datetime
from typing import Optional

import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy.orm import Mapped

from api.src.main.db import generic_db


class Plan(generic_db.Base):
    """Datatable to manage a plan"""

    __tablename__ = "plans"

    ID: Mapped[str] = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    name: Mapped[str] = sqlalchemy.Column(sqlalchemy.String)
    date: Mapped[datetime] = sqlalchemy.Column(sqlalchemy.DateTime)
    distance: Mapped[float] = sqlalchemy.Column(sqlalchemy.Float)
    distance_unit: Mapped[str] = sqlalchemy.Column(sqlalchemy.String)

    def __repr__(self):
        return f"Plan: {self.ID} {self.name} {self.date} {self.distance} {self.distance_unit}"

    def __eq__(self, other):
        # check for same type
        if not isinstance(other, Plan):
            return False

        return self.ID == other.ID and self.name == other.name and self.date == other.date and \
            self.distance == other.distance and self.distance_unit == other.distance_unit

    def equals_no_id(self, other):
        """
        Check to see if two plans are equal, but ignore the ID

        :param other: Other plan object
        :return: If the two plans are equal, but ignore the ID
        """

        # check for same type
        if not isinstance(other, Plan):
            return False

        return self.name == other.name and self.date == other.date and self.distance == other.distance and \
            self.distance_unit == other.distance_unit


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
                        distance_unit=distance_unit)

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

    def modify_plan(self, plan_id: str, new_name: str, new_date: datetime, new_distance: float,
                    new_distance_unit: str) -> Optional[Plan]:
        """
        Modify a plan

        :param plan_id: ID of the plan
        :param new_name: New name of the plan
        :param new_date: New date of the plan
        :param new_distance: New distance of the plan
        :param new_distance_unit: New distance unit of the plan
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
