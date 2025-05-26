from dataclasses import dataclass

from domain.exceptions import DomainException


@dataclass(eq=False)
class ValueException(DomainException):
    @property
    def message(self) -> str:
        return "Ошибка валидации value object-ов"


@dataclass(eq=False)
class TextTooLongException(ValueException):
    max_len: int
    value_len: int

    @property
    def message(self) -> str:
        return f"Текст слишком длинный: {self.value_len}, максимальная длинна {self.max_len}"


@dataclass(eq=False)
class TextTooShortException(ValueException):
    min_len: int
    value_len: int

    @property
    def message(self) -> str:
        return f"Текст слишком короткий: {self.value_len}, минимальная длинная {self.min_len}"