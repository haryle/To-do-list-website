from sqlalchemy import create_engine
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import create_session

from backend.model import Base, Project, Task


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


engine = create_engine("sqlite:///todo.sqlite", echo=True)
Base.metadata.create_all(engine)

session = create_session(engine)

first_project = Project(title="First Project")
second_project = Project(title="Second Project")
first_task = Task(title="First Task", status=False)
first_task.project = first_project

second_task = Task(title="Second Task", status=False)
second_task.project = first_project
second_task.parents.append(first_task)

session.add(first_project)
session.add(second_project)
session.commit()
session.close()
