from abc import ABC
from dataclasses import dataclass
from typing import (
    Any,
    TypeVar,
    Generic,
)


ModelType = TypeVar("ModelType", bound=Any)
SessionType = TypeVar("SessionType", bound=Any)


@dataclass
class IBaseDao(
    ABC,
    Generic[ModelType, SessionType]
): ...