from typing import Sequence
from uuid import UUID

from litestar import get
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.model import Tag, Task
from backend.router.base import BaseController, read_items_by_attrs
from backend.router.task import TaskDTO
from backend.router.utils.DTO import DTOGenerator

TagDTO = DTOGenerator[Tag](
    read_kwargs={"max_nested_depth": 1},
    write_kwargs={"exclude": {"tasks"}},
)


class TagController(BaseController[Tag]):
    path = "/tag"
    dto = TagDTO.write_dto
    return_dto = TagDTO.read_dto

    @get()
    async def get_tags(
            self,
            transaction: AsyncSession,
            name: str | None
    ) -> Sequence[Tag]:
        return await read_items_by_attrs(
            session=transaction, table=Tag, name=name
        )

    @get("/{id:uuid}/tasks", return_dto=TaskDTO.read_dto)
    async def get_tasks_by_tag(
            self,
            transaction: AsyncSession,
            id: UUID
    ) -> Sequence[Task]:
        stmt = select(Task).join_from(Task, Tag).where(Tag.id == id)
        result = await transaction.execute(stmt)
        return result.scalars().all()
