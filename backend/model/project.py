from litestar.dto import dto_field
from sqlalchemy.orm import Mapped, relationship

from backend.model.base import Base
from backend.model.task import Task


class Project(Base):
    __tablename__ = "project_table"

    title: Mapped[str]

    # Relationship
    tasks: Mapped[list["Task"]] = relationship(
        back_populates="project", lazy="selectin", info=dto_field("read-only")
    )

    def __repr__(self) -> str:
        return f"Project: {self.title}"
