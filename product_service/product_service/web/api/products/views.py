import uuid
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, status

from product_service.db.dependencies import get_product_repository, get_unit_of_work
from product_service.db.repositories.product_repository import ProductRepository
from product_service.db.unit_of_work import UnitOfWork
from product_service.services.product_service import ProductService
from product_service.web.api.products.schemas import (
    ProductCreate,
    ProductListResponse,
    ProductResponse,
    ProductUpdate,
)

router = APIRouter()


def get_product_service(
    uow: Annotated[UnitOfWork, Depends(get_unit_of_work)],
    repo: Annotated[ProductRepository, Depends(get_product_repository)],
) -> ProductService:
    return ProductService(uow, repo)


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    data: ProductCreate,
    service: Annotated[ProductService, Depends(get_product_service)],
) -> ProductResponse:
    return await service.create_product(data)


@router.get("", response_model=ProductListResponse)
async def list_products(
    service: Annotated[ProductService, Depends(get_product_service)],
    name: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
) -> ProductListResponse:
    return await service.list_products(
        name=name,
        page=page,
        page_size=page_size,
    )


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: uuid.UUID,
    service: Annotated[ProductService, Depends(get_product_service)],
) -> ProductResponse:
    return await service.get_product(product_id)


@router.patch("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: uuid.UUID,
    data: ProductUpdate,
    service: Annotated[ProductService, Depends(get_product_service)],
) -> ProductResponse:
    return await service.update_product(product_id, data)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: uuid.UUID,
    service: Annotated[ProductService, Depends(get_product_service)],
) -> None:
    await service.delete_product(product_id)
