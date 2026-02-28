import uuid
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, status

from order_service.db.dependencies import get_order_repository, get_unit_of_work
from order_service.db.models.order import OrderStatus
from order_service.db.repositories.order_repository import OrderRepository
from order_service.db.unit_of_work import UnitOfWork
from order_service.services.order_service import OrderService
from order_service.web.api.orders.schemas import (
    OrderCreate,
    OrderListResponse,
    OrderResponse,
    OrderUpdate,
)

router = APIRouter()


def get_order_service(
    uow: Annotated[UnitOfWork, Depends(get_unit_of_work)],
    repo: Annotated[OrderRepository, Depends(get_order_repository)],
) -> OrderService:
    return OrderService(uow, repo)


@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    data: OrderCreate,
    service: Annotated[OrderService, Depends(get_order_service)],
) -> OrderResponse:
    """Создать новый заказ."""
    return await service.create_order(data)


@router.get("", response_model=OrderListResponse)
async def list_orders(
    service: Annotated[OrderService, Depends(get_order_service)],
    order_status: Optional[OrderStatus] = None,
    product_id: Optional[uuid.UUID] = None,
    page: int = 1,
    page_size: int = 20,
) -> OrderListResponse:
    """Получить список заказов с фильтрацией и пагинацией."""
    return await service.list_orders(
        status=order_status,
        product_id=product_id,
        page=page,
        page_size=page_size,
    )


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: uuid.UUID,
    service: Annotated[OrderService, Depends(get_order_service)],
) -> OrderResponse:
    """Получить заказ по ID."""
    return await service.get_order(order_id)


@router.patch("/{order_id}", response_model=OrderResponse)
async def update_order(
    order_id: uuid.UUID,
    data: OrderUpdate,
    service: Annotated[OrderService, Depends(get_order_service)],
) -> OrderResponse:
    """Обновить заказ."""
    return await service.update_order(order_id, data)


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(
    order_id: uuid.UUID,
    service: Annotated[OrderService, Depends(get_order_service)],
) -> None:
    """Удалить заказ."""
    await service.delete_order(order_id)
