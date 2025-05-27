from dataclasses import dataclass

from .common import RepositoryException


@dataclass(eq=False)
class TextDoesntExistException(RepositoryException):
    @property
    def message(self) -> str:
        return "Такого текста не существует!"


@dataclass(eq=False)
class TextAlreadyExistException(RepositoryException):
    @property
    def message(self) -> str:
        return "Такой текст уже существует!"