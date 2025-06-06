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
    content: str


@dataclass
class AddTextResult(BaseResult):
    pass


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
        text: Text = self.text_entity_mapper.create_text(content=command.content)

        await self.text_service.act(text=text)

        from infra.taskiq.tasks import regenerate_cache_get_all_texts

        await regenerate_cache_get_all_texts.kiq(trace_carrier=trace_carrier)

        result = AddTextResult()

        return result