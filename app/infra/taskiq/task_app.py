from taskiq_aio_pika import AioPikaBroker

from core.settings.dev import get_settings
from infra.taskiq.middlewares import setup_middlewares


settings = get_settings()

taskiq_broker = AioPikaBroker(
    url=settings.rmq.rabbit_broker_url,
    queue_name="fastapi_app_queue",
)

setup_middlewares(broker=taskiq_broker)
