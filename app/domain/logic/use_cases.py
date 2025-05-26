from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass


@dataclass
class BaseCommand(ABC): ...


@dataclass
class BaseResult(ABC): ...


@dataclass
class BaseUseCase(ABC):
    @abstractmethod
    async def act(self, command: BaseCommand) -> BaseResult: ...


@dataclass
class IAddTextUseCase(
    ABC,
    BaseUseCase,
): ...


@dataclass
class IGetAllTextsUseCase(
    ABC,
    BaseUseCase,
): ...


@dataclass
class IGetTextByOidUseCase(
    ABC,
    BaseUseCase,
): ...


@dataclass
class IGetTextsByCountUseCase(
    ABC,
    BaseUseCase,
): ...


@dataclass
class IDeleteTextByOidUseCase(
    ABC,
    BaseUseCase,
): ...
