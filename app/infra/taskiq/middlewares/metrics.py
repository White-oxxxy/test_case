import time

from taskiq import TaskiqMiddleware
from taskiq.context import Context

from infra.metrics.custom_metrics import (
    task_duration,
    task_counter,
    task_error_counter,
    task_success_counter,
)


class MetricsMiddleWares(TaskiqMiddleware):
    async def before_task(self, context: Context) -> None:
        context.taskiq_metrics_start = time.perf_counter()

    async def after_task(self, context: Context, result=None, exc: Exception = None) -> None:
        start = getattr(context, "taskiq_metrics_start", None)

        if start is not None:
            duration = time.perf_counter() - start

            task_duration.record(duration, {"task_name": context.message.task_name})
            task_counter.add(1, {"task_name": context.message.task_name})

        if exc:
            task_error_counter.add(1, {"task_name": context.message.name})

        else:
            task_success_counter.add(1, {"task_name": context.message.name})