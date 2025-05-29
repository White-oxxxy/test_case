from fastapi import (
    FastAPI,
    Request,
)
from fastapi.responses import JSONResponse

from infra.pg.repositories.exceptions.common import EmptyDataException
from infra.pg.repositories.exceptions.text import (
    TextAlreadyExistException,
    TextDoesntExistException,
)


def setup_exception_handler(app: FastAPI) -> None:
    def _build_response(detail: str, status_code: int) -> JSONResponse:
        response = JSONResponse(
            status_code=status_code,
            content={"detail": detail}
        )

        return response

    @app.exception_handler(EmptyDataException)
    async def handle_empty_data(
        request: Request,
        exc: EmptyDataException,
    ) -> JSONResponse:
        response: JSONResponse = _build_response(
            detail=exc.message,
            status_code=404
        )

        return response

    @app.exception_handler(TextAlreadyExistException)
    async def handle_text_already_exists(
        request: Request,
        exc: TextAlreadyExistException,
    ) -> JSONResponse:
        response: JSONResponse = _build_response(
            detail=exc.message,
            status_code=409
        )

        return response

    @app.exception_handler(TextDoesntExistException)
    async def handle_text_not_found(
        request: Request,
        exc: TextDoesntExistException,
    ) -> JSONResponse:
        response: JSONResponse = _build_response(
            detail=exc.message,
            status_code=404
        )

        return response