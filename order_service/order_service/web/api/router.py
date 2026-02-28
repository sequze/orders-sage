from fastapi.routing import APIRouter

from order_service.web.api import monitoring, orders

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])
