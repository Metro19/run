"""
user_api.py
By: Zack Bamford

User API operations
"""
from datetime import datetime
from typing import Annotated

from fastapi import HTTPException, APIRouter
from fastapi.params import Depends

from api.src.main.api import models
from api.src.main.api.auth import oauth2_scheme, retrieve_user
from api.src.main.db import generic_db
from api.src.main.db.plan_db import Plan, PlanCommands

# setup
router = APIRouter()
Plan.metadata.create_all(bind=generic_db.db_obj.engine)
pc: PlanCommands = PlanCommands(generic_db.db_obj)


@router.post("/plan/create", tags=["Plan"])
def create_plan(name: str, description: str, date: datetime, distance: float, unit: str):
    """
    Creates a plan

    :param name: Name of the plan
    :param description: Description of the plan
    :param date: Final date of the plan
    :param distance: Distance of entire plan
    :param unit: Unit of the distance
    :return:
    """

    # create plan
    created_plan = pc.create_plan(name, description, date, distance, unit)

    # check for success
    if created_plan is None:
        raise HTTPException(status_code=500, detail="Failed to create plan")

    return created_plan

# TODO: Add more when admin system gets written
