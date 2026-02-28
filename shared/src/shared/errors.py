from http import HTTPStatus


class AppError(Exception):
    """Base application exception."""

    status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR
    detail: str = "Internal server error"

    def __init__(self, detail: str | None = None) -> None:
        self.detail = detail or self.__class__.detail
        super().__init__(self.detail)


class NotFoundError(AppError):
    status_code: int = HTTPStatus.NOT_FOUND
    detail: str = "Resource not found"


class ConflictError(AppError):
    status_code: int = HTTPStatus.CONFLICT
    detail: str = "Resource already exists"


class ValidationError(AppError):
    status_code: int = HTTPStatus.UNPROCESSABLE_ENTITY
    detail: str = "Validation error"
