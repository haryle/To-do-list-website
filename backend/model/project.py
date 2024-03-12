from uuid import UUID, uuid4

from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.model.base import Base
from backend.model.task import Task


class Project(Base):
    __tablename__ = "project_table"
    id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)
    title: Mapped[str]

    # Relationship
    tasks: Mapped[list["Task"]] = relationship(
        back_populates="project", lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"Project: {self.title}"



