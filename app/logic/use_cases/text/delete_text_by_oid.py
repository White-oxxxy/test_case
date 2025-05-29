from dataclasses import dataclass
from uuid import UUID

import app.infra.taskiq.tasks as tasks
from domain.infra.repositories import ITextRepositoryOrm
from domain.logic import (
    BaseUseCase,
    BaseCommand,
    BaseResult,
)


@dataclass
class DeleteTextByOidCommand(BaseCommand):
    text_oid: str


@dataclass
class DeleteTextByOidResult(BaseResult):
    pass


@dataclass
class DeleteTextByOidUseCase(BaseUseCase):
    text_repo: ITextRepositoryOrm

    async def act(self, command: DeleteTextByOidCommand) -> DeleteTextByOidResult:
        await self.text_repo.delete(text_oid=UUID(command.text_oid))
        await self.text_repo.commit()

        await tasks.regenerate_cache_get_all_texts.kiq()

        result = DeleteTextByOidResult()

        return result