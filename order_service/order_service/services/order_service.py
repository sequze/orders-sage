import uuid
from typing import Optional

from order_service.db.models.order import OrderStatus
from order_service.db.repositories.order_repository import OrderRepository
from order_service.db.unit_of_work import UnitOfWork
from order_service.exceptions import NotFoundError
from order_service.web.api.orders.schemas import (
    OrderCreate,
    OrderListResponse,
    OrderResponse,
    OrderUpdate,
)


class OrderService:

    def __init__(self, uow: UnitOfWork, repo: OrderRepository):
        self.uow = uow
        self.repo = repo

    async def create_order(self, data: OrderCreate) -> OrderResponse:
        async with self.uow as uow:
            order = await self.repo.create(
                uow.session,
                product_id=data.product_id,
                qty=data.qty,
                total=data.total,
            )
            await uow.commit()
            return OrderResponse.model_validate(order)

    async def get_order(self, order_id: uuid.UUID) -> OrderResponse:
        async with self.uow as uow:
            order = await self.repo.get_by_id(uow.session, order_id)
            if order is None:
                raise NotFoundError(f"Order {order_id} not found")
            return OrderResponse.model_validate(order)

    async def list_orders(
        self,
        status: Optional[OrderStatus] = None,
        product_id: Optional[uuid.UUID] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> OrderListResponse:
        async with self.uow as uow:
            offset = (page - 1) * page_size
            orders, total = await self.repo.get_list(
                uow.session,
                status=status,
                product_id=product_id,
                offset=offset,
                limit=page_size,
            )
            return OrderListResponse(
                items=[OrderResponse.model_validate(o) for o in orders],
                total=total,
            )

    async def update_order(self, order_id: uuid.UUID, data: OrderUpdate) -> OrderResponse:
        async with self.uow as uow:
            order = await self.repo.get_by_id(uow.session, order_id)
            if order is None:
                raise NotFoundError(f"Order {order_id} not found")
            update_data = data.model_dump(exclude_none=True)
            order = await self.repo.update(uow.session, order, **update_data)
            await uow.commit()
            return OrderResponse.model_validate(order)

    async def delete_order(self, order_id: uuid.UUID) -> None:
        async with self.uow as uow:
            order = await self.repo.get_by_id(uow.session, order_id)
            if order is None:
                raise NotFoundError(f"Order {order_id} not found")
            await self.repo.delete(uow.session, order)
            await uow.commit()


