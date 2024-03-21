from litestar.dto import dto_field
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.model.base import Base
from backend.model.task import Task


class Project(Base):
    __tablename__: str = "project_table"  # type: ignore[assignment]

    title: Mapped[str] = mapped_column(unique=True)

    # Relationship
    tasks: Mapped[list["Task"]] = relationship(
        back_populates="project",
        lazy="selectin",
        info=dto_field("read-only"),
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"Project: {self.title}"
