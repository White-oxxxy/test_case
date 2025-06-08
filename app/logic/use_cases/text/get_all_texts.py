from dataclasses import dataclass

from domain.entities import Text
from domain.infra.repositories import ITextReadRepositoryOrm
from domain.logic import (
    BaseUseCase,
    BaseCommand,
    BaseResult,
)
from infra.pg.dao import Session


@dataclass
class GetAllTextCommand(BaseCommand):
    pass


@dataclass
class GetAllTextResult(BaseResult):
    texts: list[Text]


@dataclass
class GetAllTextsUseCase(BaseUseCase):
    text_repo: ITextReadRepositoryOrm[Session]

    async def act(self, command: GetAllTextCommand) -> GetAllTextResult:
        text_entities: list[Text] = await self.text_repo.get_all()

        result = GetAllTextResult(texts=text_entities)

        return result
