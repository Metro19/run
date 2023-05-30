"""
plan_member_api.py
By: Zack Bamford

Plan member API endpoints
"""
from typing import Annotated

from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from fastapi.routing import APIRouter

from api.src.main.api import auth
from api.src.main.api.auth import oauth2_scheme
from api.src.main.db import generic_db
from api.src.main.db.plan_db import PlanCommands
from api.src.main.db.plan_member_db import PlanMember, PlanMemberCommands
from api.src.main.db.user_db import UserCommands

# setup
router = APIRouter()
PlanMember.metadata.create_all(bind=generic_db.db_obj.engine)
pc: PlanCommands = PlanCommands(generic_db.db_obj)
uc: UserCommands = UserCommands(generic_db.db_obj)
pmc: PlanMemberCommands = PlanMemberCommands(generic_db.db_obj)


@router.get("/plan/get_members", tags=["Plan"])
def get_plan_members(plan_id: str):
    """
    Retrieves all members of a plan

    :param plan_id: ID of the plan
    :return: List of plan member objects
    """

    # check for valid plan
    if pc.retrieve_plan(plan_id) is None:
        raise HTTPException(status_code=404, detail="Invalid plan ID")

    # retrieve plan members
    retrieved_members = pmc.get_all_members_for_plan(plan_id)

    return retrieved_members


@router.get("/user/get_plans", tags=["User"])
def get_user_plans(token: Annotated[str, Depends(oauth2_scheme)]):
    """
    Retrieves all plans for a user

    :param token: OAuth2 Token
    :return: List of plans for a user
    """

    # get user object
    user = auth.retrieve_user(token)

    # check for valid user
    if user is None:
        raise HTTPException(status_code=404, detail="Invalid user ID")

    # retrieve user plans
    retrieved_plans = pmc.get_all_plans_for_user(user.ID)

    return retrieved_plans
