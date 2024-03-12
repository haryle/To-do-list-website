from litestar.contrib.sqlalchemy.base import (
    AuditColumns, CommonTableAttributes
)

from sqlalchemy.orm import DeclarativeBase


class Base(AuditColumns, CommonTableAttributes, DeclarativeBase):
    pass
