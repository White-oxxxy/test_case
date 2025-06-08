from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from uuid import UUID

from .base import IBaseRepositoryOrm
from domain.entities import Text
from domain.infra.daos import SessionType


@dataclass
class ITextWriteRepositoryOrm(
    IBaseRepositoryOrm[SessionType],
    ABC,
):
    @abstractmethod
    async def add_texts(
        self,
        texts: list[Text],
    ) -> None: ...

    @abstractmethod
    async def delete(
        self,
        text_oid: UUID,
    ) -> None: ...


@dataclass
class ITextReadRepositoryOrm(
    IBaseRepositoryOrm[SessionType],
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