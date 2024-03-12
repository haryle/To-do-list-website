import uuid
from typing import Optional, TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.model.base import Base

if TYPE_CHECKING:
    from backend.model.project import Project


class TaskRelation(Base):
    __tablename__ = "task_relation_table"

    child_id: Mapped[UUID] = mapped_column(
        ForeignKey("task_table.id"), primary_key=True
    )
    parent_id: Mapped[UUID] = mapped_column(
        ForeignKey("task_table.id"), primary_key=True
    )


class Task(Base):
    __tablename__ = "task_table"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    title: Mapped[str]
    status: Mapped[bool]

    project_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("project_table.id"))

    # Relations
    project: Mapped[Optional["Project"]] = relationship(back_populates="tasks")
    children: Mapped[Optional[list["Task"]]] = relationship(
        "Task",
        secondary="task_relation_table",
        primaryjoin=id == TaskRelation.parent_id,
        secondaryjoin=id == TaskRelation.child_id,
        back_populates="parents",
        lazy="selectin"

    )
    parents: Mapped[Optional[list["Task"]]] = relationship(
        "Task",
        secondary="task_relation_table",
        primaryjoin=id == TaskRelation.child_id,
        secondaryjoin=id == TaskRelation.parent_id,
        back_populates="children",
        lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"(Task: {self.title}, Status: {self.status})"
