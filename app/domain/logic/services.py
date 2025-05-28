from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from domain.entities import Text


@dataclass
class BaseService(ABC): ...


@dataclass
class IAddTextService(
    ABC,
    BaseService,
):
    @abstractmethod
    async def act(self, text: Text) -> None: ...