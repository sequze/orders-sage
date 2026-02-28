import uuid
from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from product_service.db.models.reservation import Reservation


class ReservationRepository:
    async def create(
        self,
        session: AsyncSession,
        product_id: uuid.UUID,
        order_id: uuid.UUID,
        qty: int,
    ) -> Reservation:
        reservation = Reservation(
            product_id=product_id,
            order_id=order_id,
            qty=qty,
        )
        session.add(reservation)
        await session.flush()
        await session.refresh(reservation)
        return reservation

    async def get_by_id(
        self,
        session: AsyncSession,
        reservation_id: uuid.UUID,
    ) -> Optional[Reservation]:
        result = await session.execute(
            select(Reservation).where(Reservation.id == reservation_id)
        )
        return result.scalar_one_or_none()

    async def get_by_order_id(
        self,
        session: AsyncSession,
        order_id: uuid.UUID,
    ) -> Optional[Reservation]:
        result = await session.execute(
            select(Reservation).where(Reservation.order_id == order_id)
        )
        return result.scalar_one_or_none()

    async def get_list(
        self,
        session: AsyncSession,
        order_id: Optional[uuid.UUID] = None,
        product_id: Optional[uuid.UUID] = None,
        offset: int = 0,
        limit: int = 20,
    ) -> tuple[list[Reservation], int]:
        query = select(Reservation)
        count_query = select(func.count()).select_from(Reservation)

        if order_id is not None:
            query = query.where(Reservation.order_id == order_id)
            count_query = count_query.where(Reservation.order_id == order_id)
        if product_id is not None:
            query = query.where(Reservation.product_id == product_id)
            count_query = count_query.where(Reservation.product_id == product_id)

        total_result = await session.execute(count_query)
        total = total_result.scalar_one()

        query = query.order_by(Reservation.created_at.desc()).offset(offset).limit(limit)
        result = await session.execute(query)
        reservations = list(result.scalars().all())
        return reservations, total

    async def delete(self, session: AsyncSession, reservation: Reservation) -> None:
        await session.delete(reservation)
        await session.flush()
