import json
from dataclasses import dataclass
from typing import Any

from redis.asyncio import Redis

from domain.infra.cache import ICacheManager
from .exceptions import (
    CacheDecodeException,
    CacheEncodeException,
    ValueDoesntExistException,
)


@dataclass
class CacheManager(ICacheManager):
    redis: Redis

    async def get(
        self,
        key: str,
    ) -> dict[str, Any]:
        raw_value: bytes | None = await self.redis.get(key)
        if raw_value:
            try:
                return json.loads(raw_value)

            except json.JSONDecodeError:
                raise CacheDecodeException()

        raise ValueDoesntExistException()

    async def set(
        self,
        key: str,
        value: dict[str, Any],
        cache_exp: int,
    ) -> None:
        try:
            serializable_value: str = json.dumps(value)

        except TypeError:
            raise CacheEncodeException()

        await self.redis.set(
            name=key,
            value=serializable_value,
            ex=cache_exp
        )

    async def upsert(
        self,
        key: str,
        value: dict[str, Any],
        cache_exp: int,
    ) -> None:
        try:
            existing = await self.get(key)

            existing.update(value)

            await self.set(
                key=key,
                value=value,
                cache_exp=cache_exp,
            )

        except ValueDoesntExistException:
            await self.set(
                key=key,
                value=value,
                cache_exp=cache_exp,
            )

    async def delete(
        self,
        key: str,
    ) -> None:
        await self.redis.delete(key)