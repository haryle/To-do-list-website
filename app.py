from typing import AsyncGenerator

from advanced_alchemy.extensions.litestar.plugins.init.config.asyncio import (
    autocommit_before_send_handler,
)
from litestar import Litestar
from litestar.exceptions import ClientException
from litestar.plugins.sqlalchemy import SQLAlchemyAsyncConfig, SQLAlchemyPlugin
from litestar.status_codes import HTTP_404_NOT_FOUND, HTTP_409_CONFLICT
from sqlalchemy import Engine, event
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from backend.model import Base
from backend.router import ProjectController, TaskController


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


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
    except NoResultFound as exc:
        raise ClientException(
            status_code=HTTP_404_NOT_FOUND,
            detail="No database result matching query"
        ) from exc


db_config = SQLAlchemyAsyncConfig(
    connection_string="sqlite+aiosqlite:///todo.sqlite",
    metadata=Base.metadata,
    create_all=True,
    before_send_handler=autocommit_before_send_handler,
)

app = Litestar(
    [
        ProjectController,
        TaskController
    ],
    dependencies={"transaction": provide_transaction},
    plugins=[SQLAlchemyPlugin(db_config)],
)
