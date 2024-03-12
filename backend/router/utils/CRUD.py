import datetime
from typing import Sequence, TYPE_CHECKING

from sqlalchemy import select, update

if TYPE_CHECKING:
    from typing import Any
    from uuid import UUID
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy.orm import DeclarativeBase


async def create_item(
        session: "AsyncSession",
        data: "Any"
) -> "Any":
    session.add(data)
    return data


async def read_items_by_attrs(
        session: "AsyncSession",
        table: "DeclarativeBase",
        **kwargs
) -> Sequence["Any"]:
    stmt = select(table)
    for attr, value in kwargs.items():
        if value:
            stmt = stmt.where(table.__table__.c[attr] == value)
    result = await session.execute(stmt)
    return result.scalars().all()


async def read_item_by_id(
        session: "AsyncSession",
        table: "DeclarativeBase",
        id: "UUID"
) -> "Any":
    stmt = select(table).where(table.__table__.c.id == id)
    result = await session.execute(stmt)
    return result.scalars().one()


async def update_item(
        session: "AsyncSession",
        id: "UUID",
        data: dict,
        table: "DeclarativeBase",
) -> "Any":
    stmt = update(table).where(table.__table__.c.id == id).values(data)
    await session.execute(stmt)
    return data


async def delete_item(
        session: "AsyncSession",
        id: "UUID",
        table: "DeclarativeBase"
) -> "Any":
    item = await read_item_by_id(session=session, table=table, id=id)
    await session.delete(item)
