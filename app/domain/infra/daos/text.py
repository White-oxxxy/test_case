from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from uuid import UUID

from .base import (
    IBaseDao,
    MT,
)


@dataclass
class ITextDao(
    ABC,
    IBaseDao[MT],
):
    @abstractmethod
    async def get_by_oid(
        self,
        required_oid: UUID
    ) -> MT | None: ...

    @abstractmethod
    async def get_last_n_texts(
        self,
        count: int,
    ) -> list[MT]: ...

    @abstractmethod
    async def get_all(self) -> list[MT]: ...

    @abstractmethod
    async def create(
        self,
        content: str,
    ) -> None: ...

    @abstractmethod
    async def delete(
        self,
        text_oid: UUID,
    ) -> None: ...