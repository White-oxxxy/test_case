from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from domain.entities import Text


@dataclass
class BaseService(ABC): ...


@dataclass
class IAddTextService(BaseService):
    @abstractmethod
    async def act(self, texts: list[Text]) -> None: ...