from dataclasses import dataclass
from uuid import UUID

from domain.infra.repositories import ITextWriteRepositoryOrm
from domain.logic import (
    BaseUseCase,
    BaseCommand,
    BaseResult,
)
from infra.pg.dao import Session


@dataclass
class DeleteTextByOidCommand(BaseCommand):
    text_oid: str


@dataclass
class DeleteTextByOidResult(BaseResult):
    pass


@dataclass
class DeleteTextByOidUseCase(BaseUseCase):
    text_repo: ITextWriteRepositoryOrm[Session]

    async def act(self, command: DeleteTextByOidCommand) -> DeleteTextByOidResult:
        await self.text_repo.delete(text_oid=UUID(command.text_oid))

        await self.text_repo.commit()

        from infra.taskiq.tasks import regenerate_cache_get_all_texts

        await regenerate_cache_get_all_texts.kiq()

        result = DeleteTextByOidResult()

        return result