"""
run_db.py
By: Zack Bamford

File to test the run commands to the database
"""
from datetime import datetime
from typing import Optional

import sqlalchemy.engine.base
from sqlalchemy.orm.session import Session

from api.src.main.db import generic_db
from api.src.main.db.generic_db import db_obj
from api.src.main.db.plan_db import Run, Event


class RunCommands:
    """
    Class to handle the run commands
    """

    def __init__(self):
        """
        Create a new RunCommands object
        """

        # add to db
        Run.metadata.create_all(db_obj.engine)

        self.engine: sqlalchemy.Engine = db_obj.engine

    def create_run(self, event_id: str, date: datetime, status: str) -> Optional[Run]:
        """
        Create a new run

        :param event_id: Event ID to add run to
        :param date: Date completed on
        :param status: Status of completion
        :return: Created run if successful
        """

        with Session(self.engine) as session:
            # check for valid event
            event: Optional[Event] = session.get(Event, event_id)

            if event is None:
                return None

            # create run
            run: Run = Run(ID=generic_db.create_id("RUN"), event_id=event_id, date=date, status=status)

            # add to db
            session.add(run)
            session.commit()

            return session.get(Run, run.ID)

    def get_run(self, run_id: str) -> Optional[Run]:
        """
        Get a run from the database

        :param run_id: Run ID to get
        :return: Run if successful
        """

        with Session(self.engine) as session:
            return session.get(Run, run_id)

    def modify_run(self, run_id: str, date: datetime, status: str) -> Optional[Run]:
        """
        Modify a run in the database

        :param run_id: Run ID to modify
        :param date: Date to change to
        :param status: Status to change to
        :return: Modified run if successful
        """

        with Session(self.engine) as session:
            # get run
            run: Optional[Run] = session.get(Run, run_id)

            if run is None:
                return None

            # modify run
            run.date = date
            run.status = status

            # commit changes
            session.commit()

            return session.get(Run, run.ID)

    def delete_run(self, run_id: str) -> Optional[Run]:
        """
        Delete a run from the database

        :param run_id: Run ID to delete
        :return: Deleted run if successful
        """

        with Session(self.engine) as session:
            # get run
            run: Optional[Run] = session.get(Run, run_id)

            if run is None:
                return None

            # delete run
            session.delete(run)
            session.commit()

            return run
