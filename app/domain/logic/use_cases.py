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
    BaseUseCase,
    ABC,
): ...


@dataclass
class IGetAllTextsUseCase(
    BaseUseCase,
    ABC,
): ...


@dataclass
class IGetTextByOidUseCase(
    BaseUseCase,
    ABC,
): ...


@dataclass
class IGetTextsByCountUseCase(
    BaseUseCase,
    ABC,
): ...


@dataclass
class IDeleteTextByOidUseCase(
    BaseUseCase,
    ABC,
): ...
