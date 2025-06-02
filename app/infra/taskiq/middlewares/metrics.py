import time

from opentelemetry import trace
from opentelemetry.trace import SpanKind
from taskiq import TaskiqMiddleware
from taskiq.context import Context

from infra.monitoring.metrics.custom_metrics import (
    task_duration,
    task_counter,
    task_error_counter,
    task_success_counter,
)
from infra.monitoring.traces_exporter import tracer


class MetricsMiddleWares(TaskiqMiddleware):
    async def before_task(self, context: Context) -> None:
        span = tracer.start_span(
            name=f"task:{context.message.task_name}",
            kind=SpanKind.INTERNAL,
        )

        context.otel_span = span
        context.otel_token = trace.use_span(span, end_on_exit=True).__enter__()

        context.taskiq_metrics_start = time.perf_counter()

    async def after_task(self, context: Context, result=None, exc: Exception = None) -> None:
        start = getattr(context, "taskiq_metrics_start", None)
        span = getattr(context, "otel_span", None)
        token = getattr(context, "otel_token", None)

        label = {"task_name": context.message.task_name}

        if start is not None:
            duration = time.perf_counter() - start

            task_duration.record(duration, label)
            task_counter.add(1, label)

        if exc:
            task_error_counter.add(1, label)

        else:
            task_success_counter.add(1, label)

        if token:
            token.__exit__(None, None, None)

        if span:
            span.end()