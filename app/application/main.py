from dishka import AsyncContainer
from dishka.integrations import fastapi as fastapi_integration
from fastapi import FastAPI

from application.lifespan import lifespan
from application.api.text.handlers import router as text_router
from application.api.text.handlers import setup_exception_handler
from application.api.text.handlers.middlewares import setup_middlewares as setup_fastapi_middlewares
from di import get_container


def create_app() -> FastAPI:
    app = FastAPI(
        title="test_case_service",
        docs_url="/docs",
        description="",
        root_path="/api",
        debug=False,
        lifespan=lifespan,
    )
    app.include_router(router=text_router)

    setup_exception_handler(app=app)

    setup_fastapi_middlewares(app=app)

    container: AsyncContainer = get_container()

    fastapi_integration.setup_dishka(container=container, app=app)

    return app
