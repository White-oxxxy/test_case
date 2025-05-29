from dataclasses import dataclass
from uuid import UUID

from domain.infra.repositories import ITextRepositoryOrm
from domain.logic import (
    BaseUseCase,
    BaseCommand,
    BaseResult,
)
from infra.taskiq.tasks import regenerate_cache_get_all_texts


@dataclass
class DeleteTextByOidCommand(BaseCommand):
    text_oid: UUID


@dataclass
class DeleteTextByOidResult(BaseResult):
    pass


@dataclass
class DeleteTextByOidUseCase(BaseUseCase):
    text_repo: ITextRepositoryOrm

    async def act(self, command: DeleteTextByOidCommand) -> DeleteTextByOidResult:
        await self.text_repo.delete(text_oid=command.text_oid)
        await self.text_repo.commit()

        await regenerate_cache_get_all_texts.kiq()

        result = DeleteTextByOidResult()

        return result