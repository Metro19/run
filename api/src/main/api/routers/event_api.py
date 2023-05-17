"""
event_api.py
By: Zack Bamford

Event API operations
"""

from datetime import datetime
from typing import Annotated

from fastapi import HTTPException, APIRouter
from fastapi.params import Depends

from api.src.main.api import models
from api.src.main.api.auth import oauth2_scheme, retrieve_user
from api.src.main.db import generic_db
from api.src.main.db.event_db import EventCommands, Event
from api.src.main.db.plan_db import PlanCommands
from api.src.main.db.run_db import RunCommands

# setup
router = APIRouter()
Event.metadata.create_all(bind=generic_db.db_obj.engine)
pc: PlanCommands = PlanCommands(generic_db.db_obj)
ec: EventCommands = EventCommands(generic_db.db_obj)
rc: RunCommands = RunCommands(generic_db.db_obj)


# TODO: Restrict access to event creation to plan owners
@router.post("/event/create", tags=["Event"], response_model=models.Event)
def create_event(plan_id: str, name: str, date: datetime, distance: float, unit: str):
    """
    Creates an event

    :param plan_id: Valid plan ID
    :param name: Plan name
    :param date: Plan date
    :param distance: Plan distance
    :param unit: Plan unit
    :return:
    """

    # check for valid plan
    if pc.retrieve_plan(plan_id) is None:
        raise HTTPException(status_code=404, detail="Plan not found.")

    # create event
    created_event = ec.add_event(name, date, distance, unit, plan_id)

    # check for success
    if created_event is None:
        raise HTTPException(status_code=500, detail="Failed to create event")

    return created_event


@router.get("/event/get", tags=["Event"], response_model=models.Event)
def get_event(event_id: str):
    """
    Gets an event

    :param event_id: Valid event ID
    :return:
    """

    # get event
    event = ec.retrieve_event(event_id)

    # check for success
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    return event


@router.post("/event/modify", tags=["Event"], response_model=models.Event)
def modify_event(event_id: str, name: str, date: datetime, distance: float, unit: str):
    """
    Modifies an event

    :param event_id: Event to modify
    :param name: New name
    :param date: New date
    :param distance: New distance
    :param unit: New unit
    :return:
    """

    # check for valid event
    if ec.retrieve_event(event_id) is None:
        raise HTTPException(status_code=404, detail="Event not found.")

    # modify event
    modified_event = ec.modify_event(event_id, name, date, distance, unit)

    # check for success
    if modified_event is None:
        raise HTTPException(status_code=500, detail="Failed to modify event")

    return modified_event


@router.get("/event/runs", tags=["Event"])
def get_all_runs_from_event(event_id: str) -> list[models.Run]:
    """
    Get all run objects from an event

    :param event_id: Event to check
    :return: List of runs
    """

    # check for valid event object
    if ec.retrieve_event(event_id) is None:
        raise HTTPException(status_code=404, detail="Event not found.")

    # get all runs from event
    runs = ec.get_all_run_ids(event_id)

    # check for success getting ids
    if runs is None:
        raise HTTPException(status_code=500, detail="Failed to get runs from event")

    # retrieve run objects from ids

    return runs


@router.delete("/event/delete", tags=["Event"])
def delete_event(event_id: str):
    """
    Deletes an event

    :param event_id: Valid event ID
    :return:
    """

    # check for valid event
    if ec.retrieve_event(event_id) is None:
        raise HTTPException(status_code=404, detail="Event not found.")

    # delete event
    deleted_event = ec.delete_event(event_id)

    # check for success
    if deleted_event is False:
        raise HTTPException(status_code=500, detail="Failed to delete event")

    return deleted_event
