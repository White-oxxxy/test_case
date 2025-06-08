from dataclasses import dataclass

from sqlalchemy.exc import IntegrityError

from domain.entities import Text
from domain.infra.repositories import ITextWriteRepositoryOrm
from domain.logic.services import IAddTextService
from infra.pg.dao import Session
from infra.pg.repositories.exceptions.text import TextAlreadyExistException


@dataclass
class AddTextService(IAddTextService):
    text_repo: ITextWriteRepositoryOrm[Session]

    async def act(self, texts: list[Text]) -> None:
        try:
            await self.text_repo.add_texts(texts=texts)
            await self.text_repo.commit()

        except IntegrityError:
            raise TextAlreadyExistException()
