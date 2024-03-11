from typing import TYPE_CHECKING, AsyncGenerator

from advanced_alchemy.extensions.litestar.plugins.init.config.asyncio import (
    autocommit_before_send_handler,
)
from controller import TaskController
from litestar import Litestar
from litestar.exceptions import ClientException
from litestar.plugins.sqlalchemy import SQLAlchemyAsyncConfig, SQLAlchemyPlugin
from litestar.status_codes import HTTP_409_CONFLICT
from model import Base
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


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


db_config = SQLAlchemyAsyncConfig(
    connection_string="sqlite+aiosqlite:///todo.sqlite",
    metadata=Base.metadata,
    create_all=True,
    before_send_handler=autocommit_before_send_handler,
)

app = Litestar(
    [TaskController],
    dependencies={"transaction": provide_transaction},
    plugins=[SQLAlchemyPlugin(db_config)],
)
