import datetime
from typing import AsyncGenerator, Optional, Sequence
from uuid import UUID

from advanced_alchemy.extensions.litestar.plugins.init.config.asyncio import (
    autocommit_before_send_handler,
)

# from controller import TaskController
from litestar import Controller, Litestar, get, post
from litestar.contrib.sqlalchemy.base import (
    AuditColumns,
)
from litestar.contrib.sqlalchemy.base import (
    UUIDAuditBase as _UUIDAuditBase,
)
from litestar.contrib.sqlalchemy.base import (
    UUIDBase as _UUIDBase,
)
from litestar.exceptions import ClientException
from litestar.plugins.sqlalchemy import SQLAlchemyAsyncConfig, SQLAlchemyPlugin
from litestar.status_codes import HTTP_409_CONFLICT

# from model import TaskTable
from sqlalchemy import ForeignKey, select

# from model import Base
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


async def provide_transaction(
    db_session: AsyncSession,
) -> AsyncGenerator[AsyncSession, None]:
    try:
        async with db_session.begin():
            yield db_session
    except IntegrityError as exc:
        raise ClientException(
            status_code=HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


class Base(DeclarativeBase):
    pass


class UUIDAuditBase(_UUIDAuditBase, DeclarativeBase):
    registry = Base.registry


class UUIDBase(_UUIDBase, DeclarativeBase):
    registry = Base.registry


class ProjectTable(UUIDAuditBase):
    title: Mapped[str]
    deadline: Mapped[Optional[datetime.datetime]]
    tasks: Mapped[list["TaskTable"]] = relationship(back_populates="project")

    def __repr__(self) -> str:
        return f"Project: {self.title}"


class TaskRelation(Base, AuditColumns):
    __tablename__ = "task_relation_table"

    child_id: Mapped[UUID] = mapped_column(
        ForeignKey("task_table.id"), primary_key=True
    )
    parent_id: Mapped[UUID] = mapped_column(
        ForeignKey("task_table.id"), primary_key=True
    )


class TaskTable(UUIDAuditBase):
    title: Mapped[str]
    status: Mapped[bool]
    project_id: Mapped[UUID] = mapped_column(ForeignKey("project_table.id"))
    project: Mapped["ProjectTable"] = relationship(back_populates="tasks")
    children: Mapped[list["TaskTable"]] = relationship(
        secondary="task_relation_table",
        back_populates="parents",
        foreign_keys=[TaskRelation.parent_id],
    )
    parents: Mapped[list["TaskTable"]] = relationship(
        secondary="task_relation_table",
        back_populates="children",
        foreign_keys=[TaskRelation.child_id],
    )

    def __repr__(self) -> str:
        return f"(Task: {self.title}, Status: {self.status})"


db_config = SQLAlchemyAsyncConfig(
    connection_string="sqlite+aiosqlite:///todo.sqlite",
    metadata=Base.metadata,
    create_all=True,
    before_send_handler=autocommit_before_send_handler,
)


class TaskController(Controller):
    path: str = "/tasks"

    @get()
    async def get_tasks(self, transaction: AsyncSession) -> list:
        stmt = select(TaskTable)
        result = await transaction.execute(stmt)
        return result.scalars().all()

    # @get("/{id:uuid}")
    # async def get_task_by_id(self, id: UUID, transaction: AsyncSession) -> TaskTable:
    #     stmt = select(TaskTable).where(TaskTable.id == id)
    #     result = await transaction.execute(stmt)
    #     return result.scalars().one()

    @post()
    async def add_task(self, transaction: AsyncSession, data: TaskTable) -> TaskTable:
        transaction.add(data)
        return data


app = Litestar(
    [TaskController],
    dependencies={"transaction": provide_transaction},
    plugins=[SQLAlchemyPlugin(db_config)],
)
