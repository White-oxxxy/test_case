from abc import ABC
from dataclasses import dataclass
from typing import (
    Any,
    TypeVar,
    Generic,
)


MT = TypeVar("MT", bound=Any)


@dataclass
class IBaseDao(
    ABC,
    Generic[MT]
): ...