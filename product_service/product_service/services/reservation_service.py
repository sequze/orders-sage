import uuid
from typing import Optional

from sqlalchemy.exc import IntegrityError

from product_service.db.repositories.product_repository import ProductRepository
from product_service.db.repositories.reservation_repository import ReservationRepository
from product_service.db.unit_of_work import UnitOfWork
from product_service.exceptions import ConflictError, NotFoundError
from product_service.web.api.reservations.schemas import (
    ReservationCreate,
    ReservationListResponse,
    ReservationResponse,
)


class ReservationService:
    def __init__(
        self,
        uow: UnitOfWork,
        reservation_repo: ReservationRepository,
        product_repo: ProductRepository,
    ):
        self.uow = uow
        self.reservation_repo = reservation_repo
        self.product_repo = product_repo

    async def create_reservation(self, data: ReservationCreate) -> ReservationResponse:
        async with self.uow as uow:
            product = await self.product_repo.get_by_id(uow.session, data.product_id)
            if product is None:
                raise NotFoundError(f"Product {data.product_id} not found")
            if product.stock < data.qty:
                raise ConflictError(
                    f"Not enough stock for product {data.product_id}: "
                    f"available={product.stock}, requested={data.qty}"
                )

            try:
                reservation = await self.reservation_repo.create(
                    uow.session,
                    product_id=data.product_id,
                    order_id=data.order_id,
                    qty=data.qty,
                )
            except IntegrityError as exc:
                raise ConflictError(
                    f"Reservation for order {data.order_id} already exists",
                ) from exc

            product.stock -= data.qty
            await self.product_repo.update(uow.session, product, stock=product.stock)
            await uow.commit()
            return ReservationResponse.model_validate(reservation)

    async def get_reservation(self, reservation_id: uuid.UUID) -> ReservationResponse:
        async with self.uow as uow:
            reservation = await self.reservation_repo.get_by_id(uow.session, reservation_id)
            if reservation is None:
                raise NotFoundError(f"Reservation {reservation_id} not found")
            return ReservationResponse.model_validate(reservation)

    async def list_reservations(
        self,
        order_id: Optional[uuid.UUID] = None,
        product_id: Optional[uuid.UUID] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> ReservationListResponse:
        async with self.uow as uow:
            offset = (page - 1) * page_size
            reservations, total = await self.reservation_repo.get_list(
                uow.session,
                order_id=order_id,
                product_id=product_id,
                offset=offset,
                limit=page_size,
            )
            return ReservationListResponse(
                items=[ReservationResponse.model_validate(item) for item in reservations],
                total=total,
            )

    async def delete_reservation(self, reservation_id: uuid.UUID) -> None:
        async with self.uow as uow:
            reservation = await self.reservation_repo.get_by_id(uow.session, reservation_id)
            if reservation is None:
                raise NotFoundError(f"Reservation {reservation_id} not found")

            product = await self.product_repo.get_by_id(uow.session, reservation.product_id)
            if product is None:
                raise NotFoundError(f"Product {reservation.product_id} not found")

            product.stock += reservation.qty
            await self.product_repo.update(uow.session, product, stock=product.stock)
            await self.reservation_repo.delete(uow.session, reservation)
            await uow.commit()
