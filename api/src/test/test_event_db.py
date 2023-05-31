"""
test_event_db.py
By: Zack Bamford

File to test the event commands to the database
"""
from datetime import datetime
from unittest import TestCase

from api.src.main.db import generic_db
from api.src.main.db.event_db import EventCommands
from api.src.main.db.plan_db import PlanCommands
from api.src.main.db.db_models import Event, Plan


class TestEventCommands(TestCase):
    """
    Test the event database commands
    """

    pc: PlanCommands = PlanCommands(generic_db.db_obj)
    ec: EventCommands = EventCommands(generic_db.db_obj)

    dt = datetime.now()

    # test plan object
    VALID_PLAN = Plan(ID="x", name="x", date=dt, distance=21, distance_unit="ft")

    # test event objects
    VALID_EVENT = Event(ID="x", name="x", date=dt, distance=21, distance_unit="ft", plan_id="x")
    VALID_EVENT_2 = Event(ID="", name="", date=dt, distance=2.223, distance_unit="inch", plan_id="a")

    VALID_EVENTS = [VALID_EVENT, VALID_EVENT_2]

    UPDATE_EVENT = Event(ID="a", name="b", date=dt, distance=5, distance_unit="km", plan_id="g")

    INVALID_EVENT = Event(ID=" ", name="  ", date=dt, distance=8947456, distance_unit="light years", plan_id="")

    def test_add_event(self):
        """
        Test adding an event to the database

        :return:
        """

        # create plan
        created_plan = self.pc.create_plan(self.VALID_PLAN.name, self.VALID_PLAN.description, self.VALID_PLAN.date,
                                           self.VALID_PLAN.distance, self.VALID_PLAN.distance_unit)

        for event in self.VALID_EVENTS:
            # add to db
            created_event = self.ec.add_event(event.name, event.date, event.distance, event.distance_unit,
                                              created_plan.ID)
            self.assertTrue(created_event.equals_no_id(event))

            # check db
            retrieved_event = self.ec.retrieve_event(created_event.ID)
            self.assertTrue(retrieved_event.equals_no_id(event))

    def test_retrieve_event(self):
        """
        Test retrieving an event from the database

        :return:
        """

        # create plan
        created_plan = self.pc.create_plan(self.VALID_PLAN.name, self.VALID_PLAN.description, self.VALID_PLAN.date,
                                           self.VALID_PLAN.distance, self.VALID_PLAN.distance_unit)

        for event in self.VALID_EVENTS:
            # add to db
            created_event = self.ec.add_event(event.name, event.date, event.distance, event.distance_unit,
                                              created_plan.ID)

            # check db
            retrieved_event = self.ec.retrieve_event(created_event.ID)
            self.assertTrue(retrieved_event.equals_no_id(event))

    def test_modify_event(self):
        """
        Test modifying an event in the database

        :return:
        """

        # create plan
        created_plan = self.pc.create_plan(self.VALID_PLAN.name, self.VALID_PLAN.description, self.VALID_PLAN.date,
                                           self.VALID_PLAN.distance, self.VALID_PLAN.distance_unit)

        for event in self.VALID_EVENTS:
            # add to db
            created_event = self.ec.add_event(event.name, event.date, event.distance, event.distance_unit,
                                              created_plan.ID)

            # modify event
            modified_event = self.ec.modify_event(created_event.ID, self.UPDATE_EVENT.name, self.UPDATE_EVENT.date,
                                                  self.UPDATE_EVENT.distance, self.UPDATE_EVENT.distance_unit)

            # check db
            retrieved_event = self.ec.retrieve_event(modified_event.ID)
            self.assertTrue(retrieved_event.equals_no_id(modified_event))

    def test_delete_event(self):
        """
        Test deleting an event

        :return:
        """

        # create plan
        created_plan = self.pc.create_plan(self.VALID_PLAN.name, self.VALID_PLAN.description, self.VALID_PLAN.date,
                                           self.VALID_PLAN.distance, self.VALID_PLAN.distance_unit)

        for event in self.VALID_EVENTS:
            # add to db
            created_event = self.ec.add_event(event.name, event.date, event.distance, event.distance_unit,
                                              created_plan.ID)

            # delete event
            self.ec.delete_event(created_event.ID)

            # check db
            self.assertIsNone(self.ec.retrieve_event(created_event.ID))
