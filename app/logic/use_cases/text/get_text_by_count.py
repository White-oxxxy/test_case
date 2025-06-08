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
class GetTextsByCountCommand(BaseCommand):
    count: int


@dataclass
class GetTextsByCountResult(BaseResult):
    texts: list[Text]


@dataclass
class GetTextsByCountUseCase(BaseUseCase):
    text_repo: ITextReadRepositoryOrm[Session]

    async def act(self, command: GetTextsByCountCommand) -> GetTextsByCountResult:
        text_entities: list[Text] = await self.text_repo.get_last_n_texts(count=command.count)

        result = GetTextsByCountResult(texts=text_entities)

        return result