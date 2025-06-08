from fastapi import (
    FastAPI,
    Request,
    status,
)
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from domain.values.exceptions import (
    TextTooLongException,
    TextTooShortException,
)
from infra.pg.repositories.exceptions.common import EmptyDataException
from infra.pg.repositories.exceptions.text import (
    TextAlreadyExistException,
    TextDoesntExistException,
)
from infra.redis.exceptions import (
    CacheDecodeException,
    CacheEncodeException,
)


def setup_exception_handler(app: FastAPI) -> None:
    def _build_response(detail: str, status_code: int) -> JSONResponse:
        response = JSONResponse(
            status_code=status_code,
            content={"detail": detail}
        )

        return response

    @app.exception_handler(TextTooLongException)
    async def handel_text_too_long_exception(
        request: Request,
        exc: TextTooLongException,
    ) -> JSONResponse:
        response: JSONResponse = _build_response(
            detail=exc.message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )

        return response

    @app.exception_handler(TextTooShortException)
    async def handel_text_too_short_exception(
        request: Request,
        exc: TextTooShortException,
    ) -> JSONResponse:
        response: JSONResponse = _build_response(
            detail=exc.message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )

        return response

    @app.exception_handler(EmptyDataException)
    async def handle_empty_data(
        request: Request,
        exc: EmptyDataException,
    ) -> JSONResponse:
        response: JSONResponse = _build_response(
            detail=exc.message,
            status_code=status.HTTP_404_NOT_FOUND
        )

        return response

    @app.exception_handler(TextAlreadyExistException)
    async def handle_text_already_exists(
        request: Request,
        exc: TextAlreadyExistException,
    ) -> JSONResponse:
        response: JSONResponse = _build_response(
            detail=exc.message,
            status_code=status.HTTP_409_CONFLICT,
        )

        return response

    @app.exception_handler(TextDoesntExistException)
    async def handle_text_not_found(
        request: Request,
        exc: TextDoesntExistException,
    ) -> JSONResponse:
        response: JSONResponse = _build_response(
            detail=exc.message,
            status_code=status.HTTP_404_NOT_FOUND,
        )

        return response

    @app.exception_handler(CacheDecodeException)
    async def handel_cache_decode_exception(
        request: Request,
        exc: CacheDecodeException,
    ) -> JSONResponse:
        response: JSONResponse = _build_response(
            detail=exc.message,
            status_code=status.HTTP_400_BAD_REQUEST,
        )

        return response

    @app.exception_handler(CacheEncodeException)
    async def handel_cache_encode_exception(
        request: Request,
        exc: CacheEncodeException,
    ) -> JSONResponse:
        response: JSONResponse = _build_response(
            detail=exc.message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

        return response

    @app.exception_handler(RequestValidationError)
    async def handel_request_validation_error(
        request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        response: JSONResponse = _build_response(
            detail="Ошибка валидации запроса!",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

        return response

    @app.exception_handler(ValidationError)
    async def handel_pydantic_validation_error(
        request: Request,
        exc: ValidationError,
    ) -> JSONResponse:
        response: JSONResponse = _build_response(
            detail="Ошибка валидации пайдентика!",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

        return response

    @app.exception_handler(SQLAlchemyError)
    async def handel_db_exception(
        request: Request,
        exc: SQLAlchemyError,
    ) -> JSONResponse:
        response: JSONResponse = _build_response(
            detail="Ошибка на строне движка базы данных!",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

        return response

    @app.exception_handler(Exception)
    async def handle_generic_exception(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:
        response: JSONResponse = _build_response(
            detail="Ошибка сервера",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

        return response