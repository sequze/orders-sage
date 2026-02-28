"""Repositories for product_service."""

from product_service.db.repositories.product_repository import ProductRepository
from product_service.db.repositories.reservation_repository import ReservationRepository

__all__ = ["ProductRepository", "ReservationRepository"]
