import time
from dataclasses import dataclass
from typing import (
    TypeVar,
    Generic,
)

from opentelemetry.sdk.metrics import (
    Histogram,
    Counter,
)

from domain.infra.daos import IBaseDao
from domain.infra.cache import ICacheManager
from domain.logic.use_cases import BaseUseCase


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
                start = time.perf_counter()

                try:
                    result = await orig_attr(*args, **kwargs)

                    self.success_counter.add(1, {"dao": self.name, "method": attr})

                    return result
                except Exception:
                    self.error_counter.add(1, {"dao": self.name, "method": attr})

                    raise

                finally:
                    elapsed = time.perf_counter() - start

                    self.duration.record(elapsed, {"dao": self.name, "method": attr})

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

    def __getattr__(self, item):
        attr = getattr(self.cache_manager, item)

        if callable(attr):
            async def wrapper(*args, **kwargs):
                start = time.perf_counter()

                try:
                    result = await attr(*args, **kwargs)

                    self.success_counter.add(1, {"cache_manager": self.name, "method": item})

                    return result

                except Exception:
                    self.error_counter.add(1, {"cache_manager": self.name, "method": item})

                    raise

                finally:
                    elapsed = time.perf_counter() - start

                    self.duration.record(elapsed, {"cache_manager": self.name, "method": item})

            return wrapper

        return attr


UseCaseType = TypeVar("UseCaseType", bound=BaseUseCase)


@dataclass
class UseCaseWithMetricsProxy(Generic[UseCaseType]):
    use_case: UseCaseType
    name: str
    duration: Histogram
    counter: Counter
    success_counter: Counter
    error_counter: Counter

    def __getattr__(self, item):
        attr = getattr(self.use_case, item)

        if item == "act" and callable(attr):
            async def wrapper(*args, **kwargs):
                start = time.perf_counter()

                try:
                    result = await attr(*args, **kwargs)

                    self.success_counter.add(1, {"usecase": self.name})

                    return result

                except Exception:
                    self.error_counter.add(1, {"usecase": self.name})

                    raise

                finally:
                    elapsed = time.perf_counter() - start

                    self.duration.record(elapsed, {"usecase": self.name})
                    self.counter.add(1, {"usecase": self.name})

            return wrapper

        return attr