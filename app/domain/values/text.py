from dataclasses import dataclass

from .base import BaseValue
from domain.values.exceptions import (
    TextTooLongException,
    TextTooShortException,
)


@dataclass(frozen=True)
class ContentValue(BaseValue):
    max_len = 16
    min_len = 1

    def validate(self):
        value_len: int = len(self.value)

        if value_len < self.min_len:
            raise TextTooShortException(
                min_len=self.min_len,
                value_len=value_len,
            )

        if value_len > self.max_len:
            raise TextTooLongException(
                max_len=self.max_len,
                value_len=value_len,
            )

    def as_genetic_type(self) -> str:
        return str(self.value)