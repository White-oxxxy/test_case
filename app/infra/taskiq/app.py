import taskiq_fastapi
from taskiq_aio_pika import AioPikaBroker
from taskiq_redis import RedisAsyncResultBackend

from core.settings.dev import get_settings


settings = get_settings()


taskiq_broker = (
    AioPikaBroker(url=settings.rmq.rabbit_broker_url)
    .with_result_backend(RedisAsyncResultBackend(redis_url=settings.redis.redis_url))
)

taskiq_fastapi.init(broker=taskiq_broker, app_or_path="app.application.main:create_app")