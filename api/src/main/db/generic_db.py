"""
generic_db.py
By: Zack Bamford

File to manage basic database items
"""
import os
import uuid
import logging

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class DBModificationObject:
    """
    Superclass designed to create an SQLAlchemy engine for DB modification libraries
    """
    engine: sqlalchemy.Engine

    def __init__(self):
        """
        Create the object.
        Function will use DB_URL env var, or wil set to debug mode if that does not exist
        """
        try:
            self.engine = create_engine(os.environ["DB_URL"], echo=False)
        except KeyError:
            logging.info("No DB_URL environmental variable set, using debug in memory database.")
            self.engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

        # create tables
        Base.metadata.create_all(self.engine)


def create_id(object_name: str) -> str:
    """
    Create a random job ID using uuid4
    :param object_name: The object code to append to the ID
    :return: Random ID in the format of OBJECTNAME_UUID
    """
    return f"{object_name}_{str(uuid.uuid4()).strip('-')}"


# create and store the DB modification object
db_obj: DBModificationObject = DBModificationObject()