import uuid
from typing import Optional

from product_service.db.repositories.product_repository import ProductRepository
from product_service.db.unit_of_work import UnitOfWork
from product_service.exceptions import NotFoundError
from product_service.web.api.products.schemas import (
    ProductCreate,
    ProductListResponse,
    ProductResponse,
    ProductUpdate,
)


class ProductService:
    def __init__(self, uow: UnitOfWork, repo: ProductRepository):
        self.uow = uow
        self.repo = repo

    async def create_product(self, data: ProductCreate) -> ProductResponse:
        async with self.uow as uow:
            product = await self.repo.create(
                uow.session,
                name=data.name,
                stock=data.stock,
            )
            await uow.commit()
            return ProductResponse.model_validate(product)

    async def get_product(self, product_id: uuid.UUID) -> ProductResponse:
        async with self.uow as uow:
            product = await self.repo.get_by_id(uow.session, product_id)
            if product is None:
                raise NotFoundError(f"Product {product_id} not found")
            return ProductResponse.model_validate(product)

    async def list_products(
        self,
        name: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> ProductListResponse:
        async with self.uow as uow:
            offset = (page - 1) * page_size
            products, total = await self.repo.get_list(
                uow.session,
                name=name,
                offset=offset,
                limit=page_size,
            )
            return ProductListResponse(
                items=[ProductResponse.model_validate(p) for p in products],
                total=total,
            )

    async def update_product(
        self,
        product_id: uuid.UUID,
        data: ProductUpdate,
    ) -> ProductResponse:
        async with self.uow as uow:
            product = await self.repo.get_by_id(uow.session, product_id)
            if product is None:
                raise NotFoundError(f"Product {product_id} not found")

            update_data = data.model_dump(exclude_none=True)
            product = await self.repo.update(uow.session, product, **update_data)
            await uow.commit()
            return ProductResponse.model_validate(product)

    async def delete_product(self, product_id: uuid.UUID) -> None:
        async with self.uow as uow:
            product = await self.repo.get_by_id(uow.session, product_id)
            if product is None:
                raise NotFoundError(f"Product {product_id} not found")
            await self.repo.delete(uow.session, product)
            await uow.commit()
