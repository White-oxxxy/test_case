from fastapi import FastAPI

from application.lifespan import lifespan
from application.api.v1.handlers import router as text_router


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

    return app