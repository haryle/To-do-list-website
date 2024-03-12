import pdb

from sqlalchemy import create_engine
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import create_session

from backend.model.base import Base
from backend.model.project import Project

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


engine = create_engine("sqlite:///todo.sqlite", echo=True)
Base.metadata.create_all(engine)

session = create_session(engine)


