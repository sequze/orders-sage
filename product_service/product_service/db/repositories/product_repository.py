import uuid
from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from product_service.db.models.product import Product


class ProductRepository:
    async def create(self, session: AsyncSession, name: str, stock: int) -> Product:
        product = Product(name=name, stock=stock)
        session.add(product)
        await session.flush()
        await session.refresh(product)
        return product

    async def get_by_id(
        self,
        session: AsyncSession,
        product_id: uuid.UUID,
    ) -> Optional[Product]:
        result = await session.execute(select(Product).where(Product.id == product_id))
        return result.scalar_one_or_none()

    async def get_list(
        self,
        session: AsyncSession,
        name: Optional[str] = None,
        offset: int = 0,
        limit: int = 20,
    ) -> tuple[list[Product], int]:
        query = select(Product)
        count_query = select(func.count()).select_from(Product)

        if name is not None:
            search = f"%{name}%"
            query = query.where(Product.name.ilike(search))
            count_query = count_query.where(Product.name.ilike(search))

        total_result = await session.execute(count_query)
        total = total_result.scalar_one()

        query = query.order_by(Product.created_at.desc()).offset(offset).limit(limit)
        result = await session.execute(query)
        products = list(result.scalars().all())
        return products, total

    async def update(self, session: AsyncSession, product: Product, **kwargs) -> Product:
        for key, value in kwargs.items():
            setattr(product, key, value)
        await session.flush()
        await session.refresh(product)
        return product

    async def delete(self, session: AsyncSession, product: Product) -> None:
        await session.delete(product)
        await session.flush()
