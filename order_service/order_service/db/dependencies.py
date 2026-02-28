from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from .db_helper import db_helper
from .repositories.order_repository import OrderRepository
from .unit_of_work import UnitOfWork


def get_unit_of_work() -> UnitOfWork:
    return UnitOfWork(db_helper.session_factory)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async for session in db_helper.session_getter():
        yield session


def get_order_repository() -> OrderRepository:
    return OrderRepository()

