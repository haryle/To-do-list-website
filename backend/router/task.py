from typing import Sequence
from uuid import UUID

from litestar import get, put
from sqlalchemy.ext.asyncio import AsyncSession

from backend.model import Task
from backend.router.base import BaseController, read_item_by_id, read_items_by_attrs
from backend.router.utils.DTO import DTOGenerator

TaskDTO = DTOGenerator[Task](
    read_kwargs={"max_nested_depth": 1},
    write_kwargs={"exclude": {"parents", "children"}},
)


class TaskController(BaseController[Task]):
    path = "/task"
    dto = TaskDTO.write_dto
    return_dto = TaskDTO.read_dto

    @get()
    async def get_tasks(
            self,
            transaction: AsyncSession,
            title: str | None = None,
            status: bool | None = None
    ) -> Sequence[Task]:
        return await read_items_by_attrs(
            session=transaction, table=Task, title=title, status=status
        )

    @get("/children/{id:uuid}")
    async def get_children_tasks(
            self,
            transaction: AsyncSession,
            id: UUID
    ) -> Sequence[Task]:
        task = await read_item_by_id(session=transaction, table=Task, id=id)
        return task.children

    @get("/parents/{id:uuid}")
    async def get_parent_tasks(
            self,
            transaction: AsyncSession,
            id: UUID
    ) -> Sequence[Task]:
        task = await read_item_by_id(session=transaction, table=Task, id=id)
        return task.parents

    @put("/set_relation")
    async def set_relationship(
            self, child_id: UUID, parent_id: UUID, transaction: AsyncSession
            ) -> Task:
        child_task: Task = await read_item_by_id(
            session=transaction, table=Task, id=child_id
            )
        parent_task: Task = await read_item_by_id(
            session=transaction, table=Task, id=parent_id
            )
        if parent_task not in child_task.parents:
            child_task.parents.append(parent_task)
        return child_task

    @put("/remove_relation")
    async def remove_relationship(
            self, child_id: UUID, parent_id: UUID, transaction: AsyncSession
    ) -> Task:
        child_task: Task = await read_item_by_id(
            session=transaction, table=Task, id=child_id
        )
        parent_task: Task = await read_item_by_id(
            session=transaction, table=Task, id=parent_id
        )
        if parent_task in child_task.parents:
            child_task.parents.remove(parent_task)
        return child_task
