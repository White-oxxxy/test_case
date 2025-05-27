from dataclasses import dataclass

from domain.exceptions import InfraException


@dataclass(eq=False)
class RepositoryException(InfraException):
    @property
    def message(self) -> str:
        return "Произошла ошибка обработки запроса!"


@dataclass
class EmptyDataException(RepositoryException):
    @property
    def message(self) -> str:
        return "Записи отсутствуют!"