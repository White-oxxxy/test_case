from dataclasses import dataclass
from typing import Any

from domain.entities import Text
from domain.infra.repositories import ITextRepositoryOrm
from domain.infra.cache import ICacheManager
from domain.logic import (
    BaseUseCase,
    BaseCommand,
    BaseResult,
)
from infra.redis.keys import TextByCount
from infra.redis.exceptions import ValueDoesntExistException


@dataclass
class GetTextsByCountCommand(BaseCommand):
    cache_exp: int
    count: int


@dataclass
class GetTextsByCountResult(BaseResult):
    texts: list[Text]


@dataclass
class GetTextsByCountUseCase(BaseUseCase):
    text_repo: ITextRepositoryOrm
    cache_manager: ICacheManager

    async def act(self, command: GetTextsByCountCommand) -> GetTextsByCountResult:
        cache_key: str = TextByCount(count=command.count).message
        cache_result: dict[str, dict[str, Any]] | None = await self._get_cache(key=cache_key)

        if not cache_result:
            text_entities: list[Text] = await self.text_repo.get_last_n_texts(count=command.count)

            serializable_texts: dict[str, dict[str, Any]] = {}

            for text in text_entities:
                serializable_texts[str(text.oid)] = text.to_dict()

            await self.cache_manager.set(
                key=cache_key,
                value=serializable_texts,
                cache_exp=command.cache_exp,
            )
        else:
            text_entities: list[Text] = []
            for value in cache_result.values():
                text_entity: Text = Text.from_dict(data=value)

                text_entities.append(text_entity)

        result = GetTextsByCountResult(texts=text_entities)

        return result

    async def _get_cache(self, key: str) -> dict[str, dict[str, Any]] | None:
        try:
            result: dict = await self.cache_manager.get(key=key)

        except ValueDoesntExistException:
            return None

        return result