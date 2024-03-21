from typing import Sequence
from uuid import UUID

from litestar import get
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.model import Task
from backend.model.project import Project
from backend.router.base import BaseController
from backend.router.utils.DTO import DTOGenerator
from litestar.contrib.sqlalchemy.dto import SQLAlchemyDTO, SQLAlchemyDTOConfig

ProjectDTO = DTOGenerator[Project]()


class ProjectTaskDTO(SQLAlchemyDTO[Project]):
    config = SQLAlchemyDTOConfig(
        max_nested_depth=1,
        include={
            "title",
            "id",
            "tasks.0.id",
            "tasks.0.title",
            "tasks.0.status",
            "tasks.0.deadline",
            "tasks.0.description",
        },
    )


class ProjectController(BaseController[Project]):
    path = "/project"
    dto = ProjectDTO.write_dto
    return_dto = ProjectDTO.read_dto

    @get()
    async def get_projects(
        self, transaction: AsyncSession, title: str | None = None
    ) -> Sequence[Project]:
        stmt = select(Project)
        if title:
            stmt = stmt.where(Project.title == title)
        result = await transaction.execute(stmt)
        return result.scalars().all()

    @get("/{id:uuid}/tasks", return_dto=ProjectTaskDTO)
    async def get_project_tasks(self, transaction: AsyncSession, id: UUID) -> Project:
        stmt = select(Project).outerjoin(Task).where(Project.id == id).distinct()
        result = await transaction.execute(stmt)
        processed = result.scalars().one()
        return processed
