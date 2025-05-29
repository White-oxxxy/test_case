from dataclasses import dataclass

import app.infra.taskiq.tasks as tasks
from domain.entities import Text
from domain.mappers import TextEntityMapper
from domain.logic.services import IAddTextService
from domain.logic import (
    BaseUseCase,
    BaseCommand,
    BaseResult,
)


@dataclass
class AddTextCommand(BaseCommand):
    content: str


@dataclass
class AddTextResult(BaseResult):
    pass


@dataclass
class AddTextUseCase(BaseUseCase):
    text_service: IAddTextService
    text_entity_mapper: TextEntityMapper

    async def act(self, command: AddTextCommand) -> AddTextResult:
        text: Text = self.text_entity_mapper.create_text(content=command.content)

        await self.text_service.act(text=text)

        await tasks.regenerate_cache_get_all_texts.kiq()

        result = AddTextResult()

        return result