from functools import wraps
from typing import (
    Callable,
    Any,
)

from opentelemetry import propagate


def with_trace_carrier(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        trace_carrier: dict[str, str] = {}

        propagate.inject(trace_carrier)

        kwargs['trace_carrier'] = trace_carrier

        return await func(*args, **kwargs)

    return wrapper