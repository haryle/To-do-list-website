# import pdb
# from dataclasses import dataclass
# from uuid import UUID
#
# from litestar import Controller, get, post
# from sqlalchemy import select
# from sqlalchemy.ext.asyncio import AsyncSession
# from litestar.contrib.sqlalchemy.dto import SQLAlchemyDTO, SQLAlchemyDTOConfig
# from model import TaskTable
# from pydantic import TypeAdapter
#
#
# class TaskReadDTO(SQLAlchemyDTO[TaskTable]):
#     config = SQLAlchemyDTOConfig(
#         exclude={"children", "parents", "project_id", "project"}
#         )
#
# @dataclass
# class Task:
#     id: UUID
#     title: str
#     status: bool
#     project_id: UUID | None
#     children: list["Task"] | None
#     parents: list["Task"] | None
#
#
# class TaskController(Controller):
#     path: str = "/tasks"
#
#     @get(return_dto=TaskReadDTO)
#     async def get_tasks(self, transaction: AsyncSession) -> list[TaskTable]:
#         stmt = select(TaskTable)
#         result = await transaction.execute(stmt)
#         extracted = result.scalars().all()
#         return extracted
#
#     @get("/{id:uuid}")
#     async def get_task_by_id(self, id: UUID, transaction: AsyncSession) -> Task:
#         stmt = select(TaskTable).where(TaskTable.id == id)
#         result = await transaction.execute(stmt)
#         adapter = TypeAdapter(Task)
#         return adapter.dump_python(result.scalars().one())
#
#     @post()
#     async def add_task(self, transaction: AsyncSession, data: TaskTable) -> TaskTable:
#         transaction.add(data)
#         return data
