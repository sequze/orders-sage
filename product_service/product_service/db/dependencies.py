from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from product_service.db.repositories.product_repository import ProductRepository
from product_service.db.repositories.reservation_repository import ReservationRepository
from product_service.db.unit_of_work import UnitOfWork


async def get_db_session(request: Request) -> AsyncGenerator[AsyncSession]:
    """
    Create and get database session.

    :param request: current request.
    :yield: database session.
    """
    session: AsyncSession = request.app.state.db_session_factory()

    try:
        yield session
    finally:
        await session.commit()
        await session.close()


def get_unit_of_work(request: Request) -> UnitOfWork:
    return UnitOfWork(request.app.state.db_session_factory)


def get_product_repository() -> ProductRepository:
    return ProductRepository()


def get_reservation_repository() -> ReservationRepository:
    return ReservationRepository()
