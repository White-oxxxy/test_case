from dataclasses import dataclass
from typing import Any

from domain.entities import Text
from domain.infra.repositories import ITextReadRepositoryOrm
from domain.infra.cache import ICacheManager
from domain.logic import (
    BaseUseCase,
    BaseCommand,
    BaseResult,
)
from infra.pg.dao import Session
from infra.redis.exceptions import ValueDoesntExistException
from infra.redis.keys import TextAll


@dataclass
class GetAllTextCommand(BaseCommand):
    cache_exp: int


@dataclass
class GetAllTextResult(BaseResult):
    texts: list[Text]


@dataclass
class GetAllTextsUseCase(BaseUseCase):
    text_repo: ITextReadRepositoryOrm[Session]
    cache_manager: ICacheManager

    async def act(self, command: GetAllTextCommand) -> GetAllTextResult:
        cache_key: str = TextAll().message
        cache_result: dict[str, dict[str, Any]] | None= await self._get_cache(key=cache_key)

        if not cache_result:
            text_entities: list[Text] = await self.text_repo.get_all()
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

        result = GetAllTextResult(texts=text_entities)

        return result

    async def _get_cache(self, key: str) -> dict[str, dict[str, Any]] | None:
        try:
            result: dict = await self.cache_manager.get(key=key)

        except ValueDoesntExistException:
            return None

        return result
