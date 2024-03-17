from typing import Sequence
from uuid import UUID

from litestar import get, put
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from backend.model import Task
from backend.router.base import BaseController, read_item_by_id, read_items_by_attrs
from backend.router.utils.DTO import DTOGenerator

TaskDTO = DTOGenerator[Task](
    read_kwargs={"max_nested_depth": 0},
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
        parent = aliased(Task)
        child = aliased(Task)
        stmt = (select(child)
                .where(child.id != id)
                .join(Task.parents.of_type(parent))
                .where(parent.id == id))
        result = await transaction.execute(stmt)
        return result.scalars().all()

    @get("/parents/{id:uuid}")
    async def get_parent_tasks(
            self,
            transaction: AsyncSession,
            id: UUID
    ) -> Sequence[Task]:
        parent = aliased(Task)
        child = aliased(Task)
        stmt = (select(parent)
                .where(parent.id != id)
                .join(Task.children.of_type(child))
                .where(child.id == id))
        result = await transaction.execute(stmt)
        return result.scalars().all()

    @put("/set_relation")
    async def set_relationship(
            self,
            child_id: UUID,
            parent_id: UUID,
            transaction: AsyncSession
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
            self,
            child_id: UUID,
            parent_id: UUID,
            transaction: AsyncSession
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
