"""
run_api.py
By: Zack Bamford

Run API operations
"""
from datetime import datetime

from fastapi import HTTPException, APIRouter

from api.src.main.db import generic_db
import api.src.main.api.models as models
from api.src.main.db.event_db import EventCommands
from api.src.main.db.run_db import RunCommands, Run
from api.src.main.db.user_db import UserCommands

# setup
router = APIRouter()
Run.metadata.create_all(bind=generic_db.db_obj.engine)
ec: EventCommands = EventCommands(generic_db.db_obj)
rc: RunCommands = RunCommands(generic_db.db_obj)
uc: UserCommands = UserCommands(generic_db.db_obj)


@router.post("/run/create", tags=["Run"], response_model=models.Run)
def create_run(event_id: str, user_id: str, date: datetime, status: str):
    """
    Creates a run

    :param event_id: Valid event_id for the run
    :param user_id: Valid user_id for the run
    :param date: Date run was completed
    :param status: Status of the run
    :return:
    """

    # check for valid event_id
    event_check = ec.retrieve_event(event_id)

    if event_check is None:
        raise HTTPException(status_code=404, detail="Event not found")

    # check for valid parent user
    user_check = uc.retrieve_user(user_id)

    if user_check is None:
        raise HTTPException(status_code=404, detail="User not found")

    # create run
    created_run = rc.create_run(event_id, user_id, date, status)

    # check for success
    if created_run is None:
        raise HTTPException(status_code=500, detail="Failed to create run")

    return created_run


@router.get("/run/info", tags=["Run"], response_model=models.Run)
def get_run(run_id: str):
    """
    Retrieves a run

    :param run_id: Valid run_id
    :return: Run object
    """

    # get run
    run = rc.get_run(run_id)

    # check for success
    if run is None:
        raise HTTPException(status_code=404, detail="Run not found")

    return run


@router.delete("/run/delete", tags=["Run"])
def delete_run(run_id: str):
    """
    Deletes a run

    :param run_id: Valid run_id
    :return: None
    """

    # delete run
    deleted_run = rc.delete_run(run_id)

    # check for success
    if not deleted_run:
        raise HTTPException(status_code=404, detail="Run not found")
    if deleted_run:
        raise HTTPException(status_code=200)
