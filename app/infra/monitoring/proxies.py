import time
from dataclasses import dataclass
from typing import (
    TypeVar,
    Generic,
)

from opentelemetry.trace import SpanKind
from opentelemetry.sdk.metrics import (
    Histogram,
    Counter,
)

from domain.infra.daos import IBaseDao
from domain.infra.cache import ICacheManager
from domain.logic.services import BaseService
from domain.logic.use_cases import BaseUseCase
from infra.monitoring.traces_exporter import tracer


DaoType = TypeVar("DaoType", bound=IBaseDao)


@dataclass
class DaoWithMetricsProxy(Generic[DaoType]):
    dao: DaoType
    name: str
    duration: Histogram
    success_counter: Counter
    error_counter: Counter

    def __getattr__(self, attr):
        orig_attr = getattr(self.dao, attr)

        if callable(orig_attr):
            async def wrapper(*args, **kwargs):
                async with tracer.start_as_current_span(name=f"dao:{self.name}", kind=SpanKind.INTERNAL):
                    start = time.perf_counter()

                    labels = {"dao": self.name, "method": attr}

                    try:
                        result = await orig_attr(*args, **kwargs)

                        self.success_counter.add(1, labels)

                        return result
                    except Exception:
                        self.error_counter.add(1, labels)

                        raise

                    finally:
                        elapsed = time.perf_counter() - start

                        self.duration.record(elapsed, labels)

            return wrapper

        else:

            return orig_attr


CacheManagerType = TypeVar("CacheManagerType", bound=ICacheManager)


@dataclass
class CacheManagerWithMetricsProxy(Generic[CacheManagerType]):
    cache_manager: CacheManagerType
    name: str
    duration: Histogram
    success_counter: Counter
    error_counter: Counter

    def __getattr__(self, attr):
        orig_attr = getattr(self.cache_manager, attr)

        if callable(attr):
            async def wrapper(*args, **kwargs):
                async with tracer.start_as_current_span(name=f"cache_manager:{self.name}", kind=SpanKind.INTERNAL):
                    start = time.perf_counter()

                    labels = {"cache_manager": self.name, "method": attr}

                    try:
                        result = await attr(*args, **kwargs)

                        self.success_counter.add(1, labels)

                        return result

                    except Exception:
                        self.error_counter.add(1, labels)

                        raise

                    finally:
                        elapsed = time.perf_counter() - start

                        self.duration.record(elapsed, labels)

            return wrapper

        return orig_attr


ServiceType = TypeVar("ServiceType", bound=BaseService)


@dataclass
class ServiceWithMetricsProxy(Generic[ServiceType]):
    service: ServiceType
    name: str
    duration: Histogram
    counter: Counter
    success_counter: Counter
    error_counter: Counter

    def __getattr__(self, attr):
        orig_attr = getattr(self.service, attr)

        if callable(attr):
            async def wrapper(*args, **kwargs):
                async with tracer.start_as_current_span(name=f"service:{self.name}", kind=SpanKind.INTERNAL):
                    start = time.perf_counter()

                    labels = {"service": self.name, "method": attr}

                    try:
                        result = await attr(*args, **kwargs)

                        self.success_counter.add(1, labels)

                        return result

                    except Exception:
                        self.error_counter.add(1, labels)

                        raise

                    finally:
                        elapsed = time.perf_counter() - start

                        self.duration.record(elapsed, labels)
                        self.counter.add(1, labels)

            return wrapper

        return orig_attr


UseCaseType = TypeVar("UseCaseType", bound=BaseUseCase)


@dataclass
class UseCaseWithMetricsProxy(Generic[UseCaseType]):
    use_case: UseCaseType
    name: str
    duration: Histogram
    counter: Counter
    success_counter: Counter
    error_counter: Counter

    def __getattr__(self, attr):
        orig_attr = getattr(self.use_case, attr)

        if callable(attr):
            async def wrapper(*args, **kwargs):
                async with tracer.start_as_current_span(name=f"use_case:{self.name}", kind=SpanKind.INTERNAL):
                    start = time.perf_counter()

                    labels = {"use_case": self.name, "method": attr}

                    try:
                        result = await attr(*args, **kwargs)

                        self.success_counter.add(1, labels)

                        return result

                    except Exception:
                        self.error_counter.add(1, labels)

                        raise

                    finally:
                        elapsed = time.perf_counter() - start

                        self.duration.record(elapsed, labels)
                        self.counter.add(1, labels)

            return wrapper

        return orig_attr