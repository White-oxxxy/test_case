from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass


@dataclass(eq=False)
class ApplicationException(ABC, Exception):
    @property
    @abstractmethod
    def message(self) -> str:
        return "Ошибка приложения!"


@dataclass(eq=False)
class DomainException(ApplicationException):
    @property
    def message(self) -> str:
        return "Доменная ошибка!"


@dataclass(eq=False)
class InfraException(ApplicationException):
    @property
    def message(self) -> str:
        return "Инфраструктурная ошибка!"


@dataclass(eq=False)
class LogicException(ApplicationException):
    @property
    def message(self) -> str:
        return "Ошибка на уровне логики!"