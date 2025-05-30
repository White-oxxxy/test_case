from taskiq_aio_pika import AioPikaBroker

from .metrics import MetricsMiddleWares


def setup_middlewares(broker: AioPikaBroker) -> None:
    broker.add_middlewares(MetricsMiddleWares())