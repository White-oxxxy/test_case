from contextlib import asynccontextmanager

from dishka import AsyncContainer
from dishka.integrations import fastapi as fastapi_integration
from dishka.integrations import taskiq as taskiq_integration
from fastapi import FastAPI

from di import get_container
from infra.taskiq.app import taskiq_broker


@asynccontextmanager
async def lifespan(app: FastAPI):
    container: AsyncContainer = await get_container()

    fastapi_integration.setup_dishka(container=container, app=app)
    taskiq_integration.setup_dishka(container=container, broker=taskiq_broker)

    try:
        await taskiq_broker.startup()
        yield
    finally:
        await taskiq_broker.shutdown()
        await container.close()