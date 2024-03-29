from typing import TYPE_CHECKING

from litestar.dto import dto_field
from sqlalchemy import Column, ForeignKey, Table, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.model import Base

if TYPE_CHECKING:
    from backend.model import Task

tag_task_relation = Table(
    "tag_task_relation",
    Base.metadata,
    Column("tag_id", UUID, ForeignKey("tag_table.id"), primary_key=True),
    Column("task_id", UUID, ForeignKey("task_table.id"), primary_key=True),
)


class Tag(Base):
    __tablename__ = "tag_table" # type: ignore[assignment]

    name: Mapped[str] = mapped_column(unique=True)

    tasks: Mapped[list["Task"]] = relationship(
        "Task",
        secondary="tag_task_relation",
        back_populates="tags",
        info=dto_field("read-only"),
        lazy="selectin"
    )
