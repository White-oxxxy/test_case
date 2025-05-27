from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from uuid import UUID

from .base import IBaseRepositoryOrm
from domain.entities import Text


@dataclass
class ITextRepositoryOrm(
    IBaseRepositoryOrm,
    ABC,
):
    @abstractmethod
    async def get_by_oid(
        self,
        required_oid: UUID,
    ) -> Text: ...

    @abstractmethod
    async def get_last_n_texts(
        self,
        count: int,
    ) -> list[Text]: ...

    @abstractmethod
    async def get_all(self) -> list[Text]: ...

    @abstractmethod
    async def create(
        self,
        text: Text,
    ) -> None: ...

    @abstractmethod
    async def delete(
        self,
        text_oid: UUID,
    ) -> None: ...