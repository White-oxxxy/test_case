from dataclasses import dataclass

from sqlalchemy.exc import IntegrityError

from domain.entities import Text
from domain.infra.repositories import ITextRepositoryOrm
from domain.logic.services import ICreateTextService
from infra.pg.repositories.exceptions.text import TextAlreadyExistException


@dataclass
class CreateTextService(ICreateTextService):
    text_repo: ITextRepositoryOrm

    async def act(self, text: Text) -> None:
        try:
            await self.text_repo.create(text=text)

        except IntegrityError:
            raise TextAlreadyExistException()
