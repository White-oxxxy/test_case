from dataclasses import dataclass
from typing import Any
from uuid import UUID

from domain.entities import Text
from domain.infra.repositories import ITextRepositoryOrm
from domain.infra.cache import ICacheManager
from domain.logic import (
    BaseUseCase,
    BaseCommand,
    BaseResult,
)
from infra.redis.exceptions import ValueDoesntExistException
from infra.redis.keys import TextByOid


@dataclass
class GetTextByOidCommand(BaseCommand):
    text_oid: UUID
    cache_exp: int


@dataclass
class GetTextByOidResult(BaseResult):
    text: Text


@dataclass
class GetTextByOidUseCase(BaseUseCase):
    text_repo: ITextRepositoryOrm
    cache_manager: ICacheManager

    async def act(self, command: GetTextByOidCommand) -> GetTextByOidResult:
        cache_key: str = TextByOid(oid=command.text_oid).message
        cache_result: dict[str, Any] | None = await self._get_cache(key=cache_key)

        if not cache_result:
            text_entity: Text = await self.text_repo.get_by_oid(required_oid=command.text_oid)

            serializable_text: dict[str, Any] = text_entity.to_dict()

            await self.cache_manager.set(
                key=cache_key,
                value=serializable_text,
                cache_exp=command.cache_exp,
            )

        else:
            text_entity: Text = Text.from_dict(data=cache_result)

        result = GetTextByOidResult(text=text_entity)

        return result

    async def _get_cache(self, key: str) -> dict[str, Any] | None:
        try:
            result: dict = await self.cache_manager.get(key=key)

        except ValueDoesntExistException:
            return None

        return result