from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from typing import (
    Any,
    TypeVar,
    Generic,
)


RedisConnection = TypeVar("RedisConnection", bound=Any)


@dataclass
class IBaseCacheManager(
    ABC,
    Generic[RedisConnection],
): ...


@dataclass
class IWriteCacheManager(
    IBaseCacheManager[RedisConnection],
    ABC,
):
    @abstractmethod
    async def set(
            self,
            key: str,
            value: dict[str, Any],
            cache_exp: int,
    ) -> None: ...

    @abstractmethod
    async def upsert(
            self,
            key: str,
            value: dict[str, Any],
            cache_exp: int,
    ) -> None: ...

    @abstractmethod
    async def delete(
            self,
            key: str,
    ) -> None: ...


@dataclass
class IReadCacheManager(
    IBaseCacheManager[RedisConnection],
    ABC,
):
    @abstractmethod
    async def get(
        self,
        key: str,
    ) -> dict[str, Any]: ...