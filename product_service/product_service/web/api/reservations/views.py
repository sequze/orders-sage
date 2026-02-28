import uuid
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, status

from product_service.db.dependencies import (
    get_product_repository,
    get_reservation_repository,
    get_unit_of_work,
)
from product_service.db.repositories.product_repository import ProductRepository
from product_service.db.repositories.reservation_repository import ReservationRepository
from product_service.db.unit_of_work import UnitOfWork
from product_service.services.reservation_service import ReservationService
from product_service.web.api.reservations.schemas import (
    ReservationCreate,
    ReservationListResponse,
    ReservationResponse,
)

router = APIRouter()


def get_reservation_service(
    uow: Annotated[UnitOfWork, Depends(get_unit_of_work)],
    reservation_repo: Annotated[
        ReservationRepository,
        Depends(get_reservation_repository),
    ],
    product_repo: Annotated[
        ProductRepository,
        Depends(get_product_repository),
    ],
) -> ReservationService:
    return ReservationService(uow, reservation_repo, product_repo)


@router.post("", response_model=ReservationResponse, status_code=status.HTTP_201_CREATED)
async def create_reservation(
    data: ReservationCreate,
    service: Annotated[ReservationService, Depends(get_reservation_service)],
) -> ReservationResponse:
    return await service.create_reservation(data)


@router.get("", response_model=ReservationListResponse)
async def list_reservations(
    service: Annotated[ReservationService, Depends(get_reservation_service)],
    order_id: Optional[uuid.UUID] = None,
    product_id: Optional[uuid.UUID] = None,
    page: int = 1,
    page_size: int = 20,
) -> ReservationListResponse:
    return await service.list_reservations(
        order_id=order_id,
        product_id=product_id,
        page=page,
        page_size=page_size,
    )


@router.get("/{reservation_id}", response_model=ReservationResponse)
async def get_reservation(
    reservation_id: uuid.UUID,
    service: Annotated[ReservationService, Depends(get_reservation_service)],
) -> ReservationResponse:
    return await service.get_reservation(reservation_id)


@router.delete("/{reservation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reservation(
    reservation_id: uuid.UUID,
    service: Annotated[ReservationService, Depends(get_reservation_service)],
) -> None:
    await service.delete_reservation(reservation_id)
