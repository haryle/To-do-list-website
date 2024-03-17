from typing import Sequence
from uuid import UUID

from litestar import get
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.model import Task
from backend.model.project import Project
from backend.router.base import BaseController
from backend.router.task import TaskDTO
from backend.router.utils.DTO import DTOGenerator

ProjectDTO = DTOGenerator[Project]()


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

    @get("/{id:uuid}/tasks", return_dto=TaskDTO.read_dto)
    async def get_project_tasks(
            self,
            transaction: AsyncSession,
            id: UUID
    ) -> Sequence[Task]:
        stmt = select(Task).join_from(Task, Project).where(Project.id == id)
        result = await transaction.execute(stmt)
        return result.scalars().all()
