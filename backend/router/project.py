from typing import Sequence, TYPE_CHECKING
from uuid import UUID

from litestar import Controller, delete, get, post, put

from backend.model.project import Project
from backend.router.utils.CRUD import (
    create_item, delete_item, read_item_by_id, read_items_by_attrs, update_item
)
from backend.router.utils.DTO import ProjectReadDTO, ProjectWriteDTO, ProjectUpdateDTO

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class ProjectController(Controller):
    path = "/project"

    @get(return_dto=ProjectReadDTO)
    async def get_project(
            self,
            transaction: "AsyncSession",
            title: str | None = None,
    ) -> Sequence[Project]:
        return await read_items_by_attrs(session=transaction, table=Project, title=title)

    @get("/{id:uuid}", return_dto=ProjectReadDTO)
    async def get_project_by_id(
            self, transaction: "AsyncSession", id: "UUID"
    ) -> Project:
        return await read_item_by_id(session=transaction, table=Project, id=id)

    @post(dto=ProjectWriteDTO, return_dto=ProjectWriteDTO)
    async def add_project(self, transaction: "AsyncSession", data: Project) -> Project:
        return await create_item(session=transaction, data=data)

    @put("/{id:uuid}", dto=ProjectUpdateDTO, return_dto=ProjectUpdateDTO)
    async def update_project(
            self, transaction: "AsyncSession", data: Project, id: "UUID"
    ) -> Project:
        filtered_data = {k: v for k, v in data.to_dict().items() if v}
        return await update_item(
            session=transaction, id=id, data=filtered_data, table=Project
            )

    @delete("/{id:uuid}", return_dto=ProjectReadDTO)
    async def remove_project(self, id: "UUID", transaction: "AsyncSession") -> None:
        return await delete_item(session=transaction, id=id, table=Project)
