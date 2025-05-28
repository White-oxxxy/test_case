from dataclasses import dataclass

from sqlalchemy.exc import IntegrityError

from domain.entities import Text
from domain.infra.repositories import ITextRepositoryOrm
from domain.logic.services import IAddTextService
from infra.pg.repositories.exceptions.text import TextAlreadyExistException


@dataclass
class AddTextService(IAddTextService):
    text_repo: ITextRepositoryOrm

    async def act(self, text: Text) -> None:
        try:
            await self.text_repo.create(text=text)
            await self.text_repo.commit()

        except IntegrityError:
            raise TextAlreadyExistException()
