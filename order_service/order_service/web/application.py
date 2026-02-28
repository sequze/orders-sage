import logging

from fastapi import FastAPI
from order_service.web.api.router import api_router
from order_service.web.lifespan import lifespan_setup
from order_service.web.middleware import ErrorHandlingMiddleware


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    app = FastAPI(
        title="order_service",
        lifespan=lifespan_setup,
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
    )

    app.add_middleware(ErrorHandlingMiddleware)

    # Main router for the API.
    app.include_router(router=api_router, prefix="/api")

    return app
