import time

from fastapi import Request
from opentelemetry.trace import SpanKind
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)
from starlette.responses import Response

from infra.monitoring.metrics.custom_metrics import (
    controller_duration,
    controller_counter,
    controller_error_counter,
    controller_success_counter,
)
from infra.monitoring.traces_exporter import tracer


class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        start = time.perf_counter()

        labels = {
            "method": request.method,
            "path": request.url.path,
        }

        with tracer.start_as_current_span(
            name=f"controller:{request.url.path}",
            kind=SpanKind.INTERNAL,
        ):
            try:
                response = await call_next(request)

                controller_success_counter.add(1, labels)

                return response

            except Exception:
                controller_error_counter.add(1, labels)

                raise

            finally:
                duration = time.perf_counter() - start

                controller_duration.record(duration, labels)
                controller_counter.add(1, labels)

