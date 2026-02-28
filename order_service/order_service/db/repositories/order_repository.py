import uuid
from decimal import Decimal
from typing import Optional

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from order_service.db.models.order import Order, OrderStatus


class OrderRepository:

    async def create(
        self,
        session: AsyncSession,
        product_id: uuid.UUID,
        qty: int,
        total: Decimal,
    ) -> Order:
        order = Order(
            product_id=product_id,
            qty=qty,
            total=total,
        )
        session.add(order)
        await session.flush()
        await session.refresh(order)
        return order

    async def get_by_id(
        self,
        session: AsyncSession,
        order_id: uuid.UUID,
    ) -> Optional[Order]:
        result = await session.execute(
            select(Order).where(Order.id == order_id)
        )
        return result.scalar_one_or_none()

    async def get_list(
        self,
        session: AsyncSession,
        status: Optional[OrderStatus] = None,
        product_id: Optional[uuid.UUID] = None,
        offset: int = 0,
        limit: int = 20,
    ) -> tuple[list[Order], int]:
        query = select(Order)
        count_query = select(func.count()).select_from(Order)

        if status is not None:
            query = query.where(Order.status == status)
            count_query = count_query.where(Order.status == status)

        if product_id is not None:
            query = query.where(Order.product_id == product_id)
            count_query = count_query.where(Order.product_id == product_id)

        total_result = await session.execute(count_query)
        total = total_result.scalar_one()

        query = query.order_by(Order.created_at.desc()).offset(offset).limit(limit)
        result = await session.execute(query)
        orders = list(result.scalars().all())

        return orders, total

    async def update(
        self,
        session: AsyncSession,
        order: Order,
        **kwargs,
    ) -> Order:
        for key, value in kwargs.items():
            setattr(order, key, value)
        await session.flush()
        await session.refresh(order)
        return order

    async def delete(self, session: AsyncSession, order: Order) -> None:
        await session.delete(order)
        await session.flush()
