from sqlalchemy.orm import DeclarativeBase

from product_service.db.meta import meta


class Base(DeclarativeBase):
    """Base for all models."""

    metadata = meta
