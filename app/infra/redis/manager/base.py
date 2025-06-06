from dataclasses import dataclass
from typing import (
    TypeVar,
    Generic,
)

from redis.asyncio import Redis

from domain.infra.cache import IBaseCacheManager


RedisConnection = TypeVar("RedisConnection", bound=Redis)


@dataclass
class BaseCacheManager(
    IBaseCacheManager[RedisConnection],
    Generic[RedisConnection],
):
    redis: RedisConnection
