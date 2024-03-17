import datetime
from typing import Optional, TYPE_CHECKING
from uuid import UUID

from litestar.dto import dto_field
from sqlalchemy import Column, ForeignKey, Table, UUID as UUID_SQL
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.model.base import Base

if TYPE_CHECKING:
    from backend.model.project import Project
    from backend.model.tag import Tag

task_relation = Table(
    "task_relation",
    Base.metadata,
    Column("parent_id", UUID_SQL, ForeignKey("task_table.id"), primary_key=True),
    Column("child_id", UUID_SQL, ForeignKey("task_table.id"), primary_key=True),
)


class Task(Base):
    __tablename__ = "task_table"

    title: Mapped[str] = mapped_column(unique=True)
    status: Mapped[bool]
    description: Mapped[Optional[str]]
    deadline: Mapped[Optional[datetime.datetime]]

    project_id: Mapped[UUID] = mapped_column(ForeignKey("project_table.id"))

    # Relations
    project: Mapped[Optional["Project"]] = relationship(
        back_populates="tasks", lazy="selectin"
    )
    children: Mapped[list["Task"]] = relationship(
        "Task",
        secondary="task_relation",
        primaryjoin="Task.id == task_relation.c.parent_id",
        secondaryjoin="Task.id == task_relation.c.child_id",
        back_populates="parents",
        info=dto_field("read-only"),
        lazy="selectin"

    )
    parents: Mapped[list["Task"]] = relationship(
        "Task",
        secondary="task_relation",
        primaryjoin="Task.id == task_relation.c.child_id",
        secondaryjoin="Task.id == task_relation.c.parent_id",
        back_populates="children",
        info=dto_field("read-only"),
        lazy="selectin"
    )

    tags: Mapped[list["Tag"]] = relationship(
        "Tag",
        secondary="tag_task_relation",
        back_populates="tasks",
        info=dto_field("read-only"),
        lazy="selectin"
    )
