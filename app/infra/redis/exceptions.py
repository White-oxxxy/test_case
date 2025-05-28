from dataclasses import dataclass

from domain.exceptions import InfraException


@dataclass(eq=False)
class CacheException(InfraException):
    @property
    def message(self) -> str:
        return "Ошибка при работе с кэшем!"


@dataclass(eq=False)
class CacheDecodeException(CacheException):
    @property
    def message(self) -> str:
        return "Невозможно декодировать!"


@dataclass(eq=False)
class CacheEncodeException(CacheException):
    @property
    def message(self) -> str:
        return "Ощибка сереализации!"


@dataclass(eq=False)
class ValueDoesntExistException(CacheException):
    @property
    def message(self) -> str:
        return "Такого значения не существует!"