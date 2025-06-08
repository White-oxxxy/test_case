from dataclasses import dataclass

from domain.entities import Text
from domain.mappers import TextEntityMapper
from domain.logic.services import IAddTextService
from domain.logic import (
    BaseUseCase,
    BaseCommand,
    BaseResult,
)
from infra.monitoring.instruments.decorators import with_trace_carrier


@dataclass
class AddTextCommand(BaseCommand):
    contents: list[str]


@dataclass
class AddTextResult(BaseResult):
    texts: list[Text]


@dataclass
class AddTextUseCase(BaseUseCase):
    text_service: IAddTextService
    text_entity_mapper: TextEntityMapper

    @with_trace_carrier
    async def act(
        self,
        command: AddTextCommand,
        trace_carrier: dict[str, str] = None,
    ) -> AddTextResult:
        text_entities: list[Text] = []

        for content in command.contents:
            text: Text = self.text_entity_mapper.create_text(content=content)

            text_entities.append(text)

        await self.text_service.act(texts=text_entities)

        result = AddTextResult(texts=text_entities)

        return result