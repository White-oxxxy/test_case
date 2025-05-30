from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.infra.taskiq.task_app import taskiq_broker


@asynccontextmanager
async def lifespan(app: FastAPI):

    try:
        await taskiq_broker.startup()
        yield
    finally:
        await taskiq_broker.shutdown()
        await app.state.dishka_container.close()
