from dishka import AsyncContainer
from dishka.integrations.taskiq import setup_dishka
from taskiq_aio_pika import AioPikaBroker

from .middlewares import MetricsMiddleWares
from core.settings.dev import get_settings
from di import get_container


settings = get_settings()

def create_broker() -> AioPikaBroker:
    broker = (
        AioPikaBroker(
            url=settings.rmq.rabbit_broker_url,
            queue_name="fastapi_app_queue",
        ).with_middlewares(MetricsMiddleWares())
    )

    container: AsyncContainer = get_container()

    setup_dishka(container=container, broker=broker)

    return broker


taskiq_broker: AioPikaBroker = create_broker()