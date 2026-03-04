from sqlalchemy.orm import DeclarativeBase

from payment_service.db.meta import meta


class Base(DeclarativeBase):
    """Base for all models."""

    metadata = meta
