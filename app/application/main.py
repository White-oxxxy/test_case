from dishka.integrations import fastapi as fastapi_integration
from dishka.integrations import taskiq as taskiq_integration
from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from application.lifespan import lifespan
from application.api.text.handlers import router as text_router
from application.api.text.handlers import setup_exception_handler
from application.api.text.handlers.middlewares import setup_middlewares
from di import container
from infra.taskiq.task_app import taskiq_broker


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

    setup_middlewares(app=app)

    FastAPIInstrumentor.instrument_app(app=app)

    setup_exception_handler(app=app)

    fastapi_integration.setup_dishka(container=container, app=app)
    taskiq_integration.setup_dishka(container=container, broker=taskiq_broker)

    return app