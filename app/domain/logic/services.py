from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from domain.entities import Text


@dataclass
class IAddTextService(ABC):
    @abstractmethod
    async def act(self, text: Text) -> None: ...