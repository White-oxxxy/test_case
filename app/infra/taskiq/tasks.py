from typing import Any

from dishka.integrations.taskiq import (
    inject,
    FromDishka,
)

from app.infra.taskiq.task_app import taskiq_broker
from core.settings.base import CommonSettings
from domain.entities import Text
from domain.infra.repositories import ITextRepositoryOrm
from domain.infra.cache import ICacheManager
from infra.redis.keys import TextAll


@taskiq_broker.task(task_name="regenerate_cache_get_all_texts")
@inject(patch_module=True)
async def regenerate_cache_get_all_texts(
    settings: FromDishka[CommonSettings],
    text_repo: FromDishka[ITextRepositoryOrm],
    cache_manager: FromDishka[ICacheManager],
) -> None:
    cache_key = TextAll().message

    texts: list[Text] = await text_repo.get_all()

    serializable_texts: dict[str, dict[str, Any]] = {}

    for text in texts:
        serializable_texts[str(text.oid)] = text.to_dict()

    await cache_manager.upsert(
        key=cache_key,
        value=serializable_texts,
        cache_exp=settings.redis.cache_life_time
    )