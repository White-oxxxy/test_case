from taskiq_aio_pika import AioPikaBroker

from core.settings.dev import get_settings


settings = get_settings()

taskiq_broker = AioPikaBroker(
    url=settings.rmq.rabbit_broker_url,
    queue_name="fastapi_app_queue",
)
