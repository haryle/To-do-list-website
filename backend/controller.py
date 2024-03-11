from typing import TYPE_CHECKING, Any, Sequence
from uuid import UUID

from litestar import Controller, get, post
from model import TaskTable
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class TaskController(Controller):
    path: str = "/tasks"

    @get()
    async def get_tasks(self, transaction: AsyncSession) -> Sequence[TaskTable]:
        stmt = select(TaskTable)
        result = await transaction.execute(stmt)
        return result.scalars().all()

    @get("/{id:uuid}")
    async def get_task_by_id(self, id: UUID, transaction: AsyncSession) -> TaskTable:
        stmt = select(TaskTable).where(TaskTable.id == id)
        result = await transaction.execute(stmt)
        return result.scalars().one()

    @post()
    async def add_task(self, transaction: AsyncSession, data: TaskTable) -> TaskTable:
        transaction.add(data)
        return data
