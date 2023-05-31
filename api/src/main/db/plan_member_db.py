"""
plan_member_db.py
By: Zack Bamford

Functions to modify and create plan members within the database
"""
import enum
from datetime import datetime
from typing import Optional

import sqlalchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm.base import Mapped
from sqlalchemy.orm.session import Session

from api.src.main.db import generic_db
# from api.src.main.db.plan_db import PlanCommands
# from api.src.main.db.user_db import UserCommands
from api.src.main.db.db_models import PlanMember, Plan, User, PlanPermissions




class PlanMemberCommands:
    """Database commands for a PlanMember object"""

    def __init__(self, db_obj: generic_db.DBModificationObject):
        """
        Create a new PlanMemberCommnds object

        :param db_obj: DBModificationObject to use
        """

        # add tables to db
        generic_db.Base.metadata.create_all(bind=db_obj.engine)

        self.engine: sqlalchemy.Engine = db_obj.engine

        # setup UserCommands and PlanCommands object

    def add_user_to_plan(self, user_id: str, plan_id: str, plan_permissions: PlanPermissions) -> Optional[PlanMember]:
        """
        Add a user to a plan

        :param user_id: ID of user to add
        :param plan_id: ID of plan to add user to
        :param plan_permissions: Permission level of the user
        """

        with Session(self.engine) as session:

            # check for valid user object
            user = session.get(User, user_id)

            if user is None:
                return None

            # check for valid plan object
            plan = session.get(Plan, plan_id)

            if plan is None:
                return None

            # check if user is already in plan
            if self.check_if_user_in_plan(user_id, plan_id) is not None:
                return None

            # add user
            new_pm = PlanMember(ID=generic_db.create_id("PLAN_MEMBER"), user_id=user_id, plan_id=plan_id,
                                permission=plan_permissions)

            session.add(new_pm)

            session.commit()

            return session.get(PlanMember, new_pm.ID)

    def remove_user_from_plan(self, user_id: str, plan_id: str) -> bool:
        """
        Remove a user from a plan

        :param user_id: User ID to remove
        :param plan_id: Plan ID to remove from
        :return: True if successful, otherwise False
        """

        with Session(self.engine) as session:

            # check for valid user object
            user = session.get(User, user_id)

            if user is None:
                return False

            # check for valid plan object
            plan = session.get(Plan, plan_id)

            if plan is None:
                return False

            # check if user is already in plan
            pm: PlanMember = self.check_if_user_in_plan(user_id, plan_id)

            if pm is None:
                return False

            session.delete(pm)

            return True

    def get_all_members_for_plan(self, plan_id: str) -> Optional[list[User]]:
        """
        Get all users in a plan

        :param plan_id: Valid plan ID to check
        :return:
        """

        with Session(self.engine) as session:
            # get plan
            plan: Plan = session.get(Plan, plan_id)

            if plan is None:
                return None

    def get_all_plans_for_user(self, user_id: str) -> Optional[list[Plan]]:
        """
        Get all plans for a user

        :param user_id: Valid user ID to check
        :return:
        """

        with Session(self.engine) as session:
            # get user
            user: User = session.get(User, user_id)

            if user is None:
                return None

            # get all plan members for user
            plan_members: list[PlanMember] = user.plans

            plans: list[Plan] = []

            for pm in plan_members:
                plans.append(session.get(Plan, pm.plan_id))

            return plans

    def check_if_user_in_plan(self, user_id: str, plan_id: str) -> Optional[PlanMember]:
        """
        Check if a user is in a plan

        :pre: User and plan must exist

        :param user_id: User ID to check
        :param plan_id: Plan ID to check
        :return: PlanPermissions if valid, otherwise None
        """

        with Session(self.engine) as session:
            plan: Plan = session.get(Plan, plan_id)

            # check for valid plan object
            if plan is None:
                return None

            for pm in plan.plan_members:
                if pm.user_id == user_id:
                    return pm


# if __name__ == "__main__":
#     db = generic_db.db_obj
#
#     user_commands = UserCommands(db)
#     plan_member_commands = PlanMemberCommands(db)
#     plan_commands = PlanCommands(db)
#
#     u = user_commands.create_user("test", "test", "test")
#     p = plan_commands.create_plan("test", "test", datetime.now(), 123.123, "test")
#     p2 = plan_commands.create_plan("test2", "test2", datetime.now(), 123.123, "test2")
#
#     print(plan_member_commands.add_user_to_plan(u.ID, p.ID, PlanPermissions.OWNER).ID)
#     print(plan_member_commands.add_user_to_plan(u.ID, p2.ID, PlanPermissions.OWNER).ID)
#     print(plan_member_commands.get_all_plans_for_user(u.ID))
