from typing import Any

from dishka.integrations.taskiq import (
    FromDishka,
    inject,
)

from core.settings.base import CommonSettings
from domain.entities import Text
from domain.infra.repositories import ITextReadRepositoryOrm
from domain.infra.cache import IWriteCacheManager
from infra.taskiq.task_app import taskiq_broker
from infra.redis.keys import TextAll


@taskiq_broker.task(task_name="regenerate_cache_get_all_texts")
@inject(patch_module=True)
async def regenerate_cache_get_all_texts(
    settings: FromDishka[CommonSettings],
    text_repo: FromDishka[ITextReadRepositoryOrm],
    cache_manager: FromDishka[IWriteCacheManager],
    trace_carrier: dict[str, str] | None = None,
) -> None:
    cache_key = TextAll().message

    texts: list[Text] = await text_repo.get_all()

    serializable_texts: dict[str, dict[str, Any]] = {
        str(text.oid): text.to_dict() for text in texts
    }

    await cache_manager.upsert(
        key=cache_key,
        value=serializable_texts,
        cache_exp=settings.redis.cache_life_time
    )