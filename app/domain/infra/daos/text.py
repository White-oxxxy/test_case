from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from uuid import UUID

from .base import (
    IBaseDao,
    ModelType,
    SessionType,
)


@dataclass
class ITextWriteDao(
    IBaseDao[ModelType, SessionType],
    ABC,
):
    @abstractmethod
    async def add_texts(
        self,
        oids: list[UUID],
        contents: list[str],
    ) -> None: ...

    @abstractmethod
    async def delete(
        self,
        text_oid: UUID,
    ) -> ModelType | None: ...


@dataclass
class ITextReadDao(
    IBaseDao[ModelType, SessionType],
    ABC,
):
    @abstractmethod
    async def get_by_oid(
        self,
        required_oid: UUID
    ) -> ModelType | None: ...

    @abstractmethod
    async def get_last_n_texts(
        self,
        count: int,
    ) -> list[ModelType]: ...

    @abstractmethod
    async def get_all(self) -> list[ModelType]: ...