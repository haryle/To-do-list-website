import datetime
from typing import Optional
from uuid import UUID

from litestar.contrib.sqlalchemy.base import (
    AuditColumns,
)
from litestar.contrib.sqlalchemy.base import (
    UUIDAuditBase as _UUIDAuditBase,
)
from litestar.contrib.sqlalchemy.base import (
    UUIDBase as _UUIDBase,
)
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class UUIDAuditBase(_UUIDAuditBase, DeclarativeBase):
    registry = Base.registry


class UUIDBase(_UUIDBase, DeclarativeBase):
    registry = Base.registry


class ProjectTable(UUIDAuditBase):
    title: Mapped[str]
    deadline: Mapped[Optional[datetime.datetime]]
    tasks: Mapped[list["TaskTable"]] = relationship(back_populates="project")

    def __repr__(self) -> str:
        return f"Project: {self.title}"


class TaskRelation(Base, AuditColumns):
    __tablename__ = "task_relation_table"

    child_id: Mapped[UUID] = mapped_column(
        ForeignKey("task_table.id"), primary_key=True
    )
    parent_id: Mapped[UUID] = mapped_column(
        ForeignKey("task_table.id"), primary_key=True
    )


class TaskTable(UUIDAuditBase):
    title: Mapped[str]
    status: Mapped[bool]
    project_id: Mapped[UUID] = mapped_column(ForeignKey("project_table.id"))
    project: Mapped["ProjectTable"] = relationship(back_populates="tasks")
    children: Mapped[list["TaskTable"]] = relationship(
        secondary="task_relation_table",
        back_populates="parents",
        foreign_keys=[TaskRelation.parent_id],
    )
    parents: Mapped[list["TaskTable"]] = relationship(
        secondary="task_relation_table",
        back_populates="children",
        foreign_keys=[TaskRelation.child_id],
    )

    def __repr__(self) -> str:
        return f"(Task: {self.title}, Status: {self.status})"


# class TagTable(UUIDBase):
#     title: Mapped[str]

#     def __repr__(self) -> str:
#         return f"(Tag: {self.title})"


# class TaskTagRelation(Base, AuditColumns): ...
