"""
test_run_db.py
By: Zack Bamford

File to test the run commands
"""
from datetime import datetime
from unittest import TestCase

from api.src.main.db import generic_db
from api.src.main.db.event_db import EventCommands
from api.src.main.db.plan_db import Run, Event, Plan, PlanCommands
from api.src.main.db.run_db import RunCommands


class TestRunCommands(TestCase):
    """
    Test the run commands
    """

    rc: RunCommands = RunCommands(generic_db.db_obj)
    ec: EventCommands = EventCommands(generic_db.db_obj)
    pc: PlanCommands = PlanCommands(generic_db.db_obj)

    dt = datetime.now()

    # example objects
    VALID_RUN = Run(ID="x", event_id="x", date=dt, status="x")
    VALID_RUN_2 = Run(ID="", event_id="", date=dt, status="")
    VALID_RUNS = [VALID_RUN, VALID_RUN_2]

    VALID_EVENT = Event(ID="x", plan_id="x", name="x", date=dt, distance=21, distance_unit="ft")

    VALID_PLAN = Plan(ID="x", name="x", description="x", date=dt, distance=21, distance_unit="ft", users="x")

    def test_create_run(self):
        """
        Test creating a run

        :return:
        """

        created_plan = self.pc.create_plan(self.VALID_PLAN.name, self.VALID_PLAN.description, self.VALID_PLAN.date,
                                           self.VALID_PLAN.distance, self.VALID_PLAN.distance_unit)

        created_event = self.ec.add_event(self.VALID_EVENT.name, self.VALID_EVENT.date,
                                          self.VALID_EVENT.distance, self.VALID_EVENT.distance_unit, created_plan.ID)

        for run in self.VALID_RUNS:
            # add to db
            created_run = self.rc.create_run(created_event.ID, run.date, run.status)
            self.assertTrue(created_run.equals_no_id(run))

            # check db
            self.assertTrue(self.rc.get_run(created_run.ID).equals_no_id(run))

    def test_get_run(self):
        """
        Test getting a run

        :return:
        """

        created_plan = self.pc.create_plan(self.VALID_PLAN.name, self.VALID_PLAN.description, self.VALID_PLAN.date,
                                           self.VALID_PLAN.distance, self.VALID_PLAN.distance_unit)

        created_event = self.ec.add_event(self.VALID_EVENT.name, self.VALID_EVENT.date,
                                          self.VALID_EVENT.distance, self.VALID_EVENT.distance_unit, created_plan.ID)

        for run in self.VALID_RUNS:
            # add to db
            created_run = self.rc.create_run(created_event.ID, run.date, run.status)

            # check db
            self.assertTrue(self.rc.get_run(created_run.ID).equals_no_id(run))

    def test_modify_run(self):
        """
        Test modifying a run

        :return:
        """

        created_plan = self.pc.create_plan(self.VALID_PLAN.name, self.VALID_PLAN.description, self.VALID_PLAN.date,
                                           self.VALID_PLAN.distance, self.VALID_PLAN.distance_unit)

        created_event = self.ec.add_event(self.VALID_EVENT.name, self.VALID_EVENT.date,
                                          self.VALID_EVENT.distance, self.VALID_EVENT.distance_unit, created_plan.ID)

        for run in self.VALID_RUNS:
            # add to db
            created_run = self.rc.create_run(created_event.ID, run.date, run.status)

            # modify
            created_run.status = "modified"
            self.rc.modify_run(created_run.ID, created_run.date, created_run.status)

            # check db
            self.assertTrue(self.rc.get_run(created_run.ID).equals_no_id(created_run))

    def test_delete_run(self):

        created_plan = self.pc.create_plan(self.VALID_PLAN.name, self.VALID_PLAN.description, self.VALID_PLAN.date,
                                           self.VALID_PLAN.distance, self.VALID_PLAN.distance_unit)

        created_event = self.ec.add_event(self.VALID_EVENT.name, self.VALID_EVENT.date,
                                          self.VALID_EVENT.distance, self.VALID_EVENT.distance_unit, created_plan.ID)

        for run in self.VALID_RUNS:
            # add to db
            created_run = self.rc.create_run(created_event.ID, run.date, run.status)

            # delete
            self.assertTrue(self.rc.delete_run(created_run.ID))

            # check db
            self.assertIsNone(self.rc.get_run(created_run.ID))


