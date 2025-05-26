from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from typing import (
    Any,
    Generic,
    TypeVar,
)


VT = TypeVar("VT", bound=Any)
RT = TypeVar("RT", bound=Any)


@dataclass(frozen=True)
class BaseValue(ABC, Generic[VT, RT]):
    value: VT

    def __post_init__(self):
        self.validate()

    @abstractmethod
    def validate(self): ...

    @abstractmethod
    def as_genetic_type(self) -> RT: ...