"""
user_api.py
By: Zack Bamford

User API operations
"""
from datetime import datetime
from typing import Annotated

from fastapi import HTTPException, APIRouter
from fastapi.params import Depends

from api.src.main.api import auth
from api.src.main.api.auth import oauth2_scheme, retrieve_user
from api.src.main.db import generic_db
from api.src.main.db.plan_db import Plan, PlanCommands
from api.src.main.db.plan_member_db import PlanMemberCommands, PlanPermissions
from api.src.main.db.user_db import UserCommands

# setup
router = APIRouter()
Plan.metadata.create_all(bind=generic_db.db_obj.engine)
pc: PlanCommands = PlanCommands(generic_db.db_obj)
pmc: PlanMemberCommands = PlanMemberCommands(generic_db.db_obj)
uc: UserCommands = UserCommands(generic_db.db_obj)


@router.get("/plan/get", tags=["Plan"])
def retrieve_plan(token: Annotated[str, Depends(oauth2_scheme)], plan_id):
    """
    Retrieves a plan

    :param token: OAuth2 token
    :param plan_id: ID of the plan
    :return: Plan object
    """

    # get user
    user = retrieve_user(token)

    # check if user is valid
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    # retrieve plan
    retrieved_plan = pc.retrieve_all_plans_from_user_id(user.id)

    # check for success
    if retrieved_plan is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve plan")

    return retrieved_plan


@router.post("/plan/create", tags=["Plan"])
def create_plan(token: Annotated[str, Depends(oauth2_scheme)], name: str, description: str, date: datetime, distance: float, unit: str):
    """
    Creates a plan

    :param token: OAuth2 token of user creating it
    :param name: Name of the plan
    :param description: Description of the plan
    :param date: Final date of the plan
    :param distance: Distance of entire plan
    :param unit: Unit of the distance
    :return:
    """

    # check for valid token
    user = auth.retrieve_user(token)

    if user is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    # create plan
    created_plan = pc.create_plan(name, description, date, distance, unit)

    # check for success
    if created_plan is None:
        raise HTTPException(status_code=500, detail="Failed to create plan")

    # add user as admin
    created_plan = pmc.add_user_to_plan(user.ID, created_plan.ID, PlanPermissions.OWNER)

    return created_plan


@router.post("/plan/add_users", tags=["Plan"])
def add_users(plan_id: str, users: list[str]):
    """
    Adds users to a plan

    :param plan_id: ID of the plan
    :param users: List of user IDs
    :return: Updated plan object
    """

    # check that plan exists
    if pc.retrieve_plan(plan_id) is None:
        raise HTTPException(status_code=404, detail="Plan not found.")

    # check that all users are valid
    for user in users:
        if uc.retrieve_user(user) is None:
            raise HTTPException(status_code=404, detail="One or more users not found.")

    # add users
    updated_plan = pc.add_users_to_plan(plan_id, users)

    # check for success
    if updated_plan is None:
        raise HTTPException(status_code=500, detail="Failed to add users to plan")

    return updated_plan

# TODO: Add more when admin system gets written
