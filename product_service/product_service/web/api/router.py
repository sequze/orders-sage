from fastapi.routing import APIRouter

from product_service.web.api import monitoring, products, reservations

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(
    reservations.router,
    prefix="/reservations",
    tags=["reservations"],
)
