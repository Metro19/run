"""
test_plan_db.py
By: Zack Bamford

File to test the plan commands to the database
"""

from datetime import datetime
from unittest import TestCase

import api.src.main.db.generic_db as generic_db
from api.src.main.db.plan_db import PlanCommands, Plan
from api.src.main.db.user_db import User, UserCommands


class TestPlanCommands(TestCase):
    """
    Test the plan database commands
    """

    pc: PlanCommands = PlanCommands(generic_db.db_obj)
    uc: UserCommands = UserCommands(generic_db.db_obj)

    dt = datetime.now()

    # user objects to test the list
    VALID_USER = User(ID="x", username="x", email="x", password="x")
    VALID_USER_2 = User(ID="", username="", email="", password="")

    VALID_USERS = [VALID_USER, VALID_USER_2]

    # example objects
    VALID_PLAN = Plan(ID="x", name="x", description="x", date=dt, distance=21, distance_unit="ft")
    VALID_PLAN_2 = Plan(ID="", name="", description="", date=dt, distance=2.223, distance_unit="inch")

    VALID_PLANS = [VALID_PLAN, VALID_PLAN_2]
    VALID_PLANS_USERS = [["x"], ["a", "b", "c"]]

    UPDATE_PLAN = Plan(ID="a", name="b", description="c", date=dt, distance=5, distance_unit="km")

    INVALID_PLAN = Plan(ID=" ", name="  ", description="   ", date=dt, distance=8947456, distance_unit="light years")

    USERS_TO_REMOVE = ["a", "b"]
    USERS_TO_ADD = ["d", "e"]

    def test_create_plan(self):
        """
        Test creating a plan

        :return:
        """

        for plan in self.VALID_PLANS:
            # add to db
            created_plan = self.pc.create_plan(plan.name, plan.description, plan.date, plan.distance,
                                               plan.distance_unit)
            self.assertTrue(created_plan.equals_no_id(plan))

            # check db
            retrieved_plan = self.pc.retrieve_plan(created_plan.ID)
            self.assertTrue(retrieved_plan.equals_no_id(plan))

    def test_retrieve_plan(self):
        """
        Test retrieving a plan

        :return:
        """

        for plan in self.VALID_PLANS:
            # add to db
            created_plan = self.pc.create_plan(plan.name, plan.description, plan.date, plan.distance,
                                               plan.distance_unit)

            # check db
            retrieved_plan = self.pc.retrieve_plan(created_plan.ID)
            self.assertIsNotNone(retrieved_plan)
            self.assertTrue(retrieved_plan.equals_no_id(plan))

    # def test_get_user_in_plan(self):
    #     """
    #     Test receiving the user IDs in a plan as well as the user objects
    #     Also test adding a user to a plan
    #
    #     :return:
    #     """
    #
    #     # add all users and store the UID
    #     ids = []
    #     for user in self.VALID_USERS:
    #         ids.append((self.uc.create_user(user.username, user.email, user.password)).ID)
    #
    #     # inject user list into plan for testing
    #     created_plan = self.pc.create_plan(self.VALID_PLAN.name, self.VALID_PLAN.description, self.VALID_PLAN.date,
    #                         self.VALID_PLAN.distance, self.VALID_PLAN.distance_unit)
    #
    #     self.pc.add_users_to_plan(created_plan.ID, ids)
    #
    #     # run check
    #     collected_ids: list[str] = self.pc.get_user_ids_in_plan(created_plan.ID)
    #     collected_objs: list[User] = self.pc.get_user_objects_in_plan(created_plan.ID)
    #
    #     # check to make sure the correct amount was returned
    #     self.assertEqual(len(ids), len(collected_ids))
    #     self.assertEqual(len(ids), len(collected_objs))
    #
    #     # check ids
    #     for ci in collected_ids:
    #         self.assertTrue(ci in ids)
    #
    #     # check objects
    #     for co in collected_objs:
    #         for plan_id in ids:
    #             if co.ID == plan_id:
    #                 self.assertTrue(True)
    #                 break
    #
    #
    # def test_remove_users_from_plan(self):
    #     """
    #     Test removing users from a plan
    #
    #     :return:
    #     """
    #
    #     # add all users and store the UID
    #     ids = []
    #     for user in self.VALID_USERS:
    #         ids.append((self.uc.create_user(user.username, user.email, user.password)).ID)
    #
    #     # inject user list into plan for testing
    #     created_plan = self.pc.create_plan(self.VALID_PLAN.name, self.VALID_PLAN.description, self.VALID_PLAN.date,
    #                                        self.VALID_PLAN.distance, self.VALID_PLAN.distance_unit)
    #
    #     self.pc.add_users_to_plan(created_plan.ID, ids)
    #
    #     # remove users
    #     self.pc.remove_users_from_plan(created_plan.ID, ids)
    #
    #     # check to see if all are removed
    #     self.assertEqual(0, len(self.pc.get_user_ids_in_plan(created_plan.ID)))

    def test_modify_plan(self):
        """
        Test modifying a plan

        :return:
        """

        # add to db
        created_plan = self.pc.create_plan(self.VALID_PLAN.name, self.VALID_PLAN.description, self.VALID_PLAN.date,
                                           self.VALID_PLAN.distance, self.VALID_PLAN.distance_unit)

        # modify
        self.pc.modify_plan(created_plan.ID, self.UPDATE_PLAN.name, self.UPDATE_PLAN.description, self.UPDATE_PLAN.date,
                            self.UPDATE_PLAN.distance, self.UPDATE_PLAN.distance_unit)

        # check
        retrieved_plan = self.pc.retrieve_plan(created_plan.ID)
        self.assertTrue(retrieved_plan.equals_no_id(self.UPDATE_PLAN))

    def test_delete_plan(self):
        """
        Test deleting a valid plan

        :return:
        """

        # try and delete and check
        for plan in self.VALID_PLANS:
            # add to db
            created_plan = self.pc.create_plan(plan.name, plan.description, plan.date, plan.distance,
                                               plan.distance_unit)

            # delete
            self.assertTrue(self.pc.delete_plan(created_plan.ID))

            # check
            self.assertIsNone(self.pc.retrieve_plan(created_plan.ID))
