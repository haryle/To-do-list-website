from typing import Optional, TYPE_CHECKING

from litestar.dto import dto_field
from sqlalchemy import Column, ForeignKey, Table, UUID as UUID_SQL
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID
from backend.model.base import Base

if TYPE_CHECKING:
    from backend.model.project import Project

task_relation = Table(
    "task_relation",
    Base.metadata,
    Column("parent_id", UUID_SQL, ForeignKey("task_table.id"), primary_key=True),
    Column("child_id", UUID_SQL, ForeignKey("task_table.id"), primary_key=True),
)


class Task(Base):
    __tablename__ = "task_table"

    title: Mapped[str]
    status: Mapped[bool]

    project_id: Mapped[UUID] = mapped_column(ForeignKey("project_table.id"))

    # Relations
    project: Mapped[Optional["Project"]] = relationship(back_populates="tasks", lazy="immediate")
    children: Mapped[list["Task"]] = relationship(
        "Task",
        secondary="task_relation",
        primaryjoin="Task.id == task_relation.c.parent_id",
        secondaryjoin="Task.id == task_relation.c.child_id",
        back_populates="parents",
        info=dto_field("read-only"),
        lazy="immediate"

    )
    parents: Mapped[list["Task"]] = relationship(
        "Task",
        secondary="task_relation",
        primaryjoin="Task.id == task_relation.c.child_id",
        secondaryjoin="Task.id == task_relation.c.parent_id",
        back_populates="children",
        info=dto_field("read-only"),
        lazy="immediate"
    )

    def __repr__(self) -> str:
        return f"(Task: {self.title}, Status: {self.status})"
