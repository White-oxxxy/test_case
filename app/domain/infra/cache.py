from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from typing import Any


@dataclass
class ICacheManager(ABC):
    @abstractmethod
    async def get(
        self,
        key: str,
    ) -> dict[str, Any]: ...

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