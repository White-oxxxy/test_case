from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from typing import (
    Any,
    Generic,
)

from domain.infra.daos import SessionType


@dataclass
class IBaseRepositoryOrm(
    Generic[SessionType],
    ABC,
):
    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def flush(self) -> None: ...

    @abstractmethod
    async def refresh(self, instance: Any) -> None: ...