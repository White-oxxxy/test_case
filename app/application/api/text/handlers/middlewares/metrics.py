import time

from fastapi import Request
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)
from starlette.responses import Response

from infra.metrics.custom_metrics import (
    controller_duration,
    controller_counter,
    controller_error_counter,
    controller_success_counter,
)


class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start = time.perf_counter()

        try:
            response = await call_next(request)

            controller_success_counter.add(1, {"method": request.method, "path": request.url.path})

            return response

        except Exception:
            controller_error_counter.add(1, {"method": request.method, "path": request.url.path})

            raise

        finally:
            duration = time.perf_counter() - start

            controller_duration.record(duration, {"method": request.method, "path": request.url.path})
            controller_counter.add(1, {"method": request.method, "path": request.url.path})
