from dishka.integrations.fastapi import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import (
    APIRouter,
    status,
)

from application.api.text.schemas import (
    TextSchema,
    CreateTextSchema,
    DeleteTextByOidInSchema,
    GetAllTextsOutSchema,
    GetTextsByCountOutSchema,
    GetTextByOidOutSchema,
)
from core.settings.base import CommonSettings
from logic.use_cases import (
    AddTextUseCase,
    AddTextCommand,
    DeleteTextByOidUseCase,
    DeleteTextByOidCommand,
    GetAllTextsUseCase,
    GetAllTextCommand,
    GetAllTextResult,
    GetTextsByCountUseCase,
    GetTextsByCountCommand,
    GetTextsByCountResult,
    GetTextByOidUseCase,
    GetTextByOidCommand,
    GetTextByOidResult,
)


router = APIRouter(prefix="/text")


@router.post(
    path="/new",
    status_code=status.HTTP_201_CREATED,
    description="Создание нового текста",
)
@inject
async def add_text_handler(
    schema: CreateTextSchema,
    use_case: FromDishka[AddTextUseCase],
) -> None:
    command = AddTextCommand(content=schema.content)

    await use_case.act(command=command)


@router.delete(
    path="/{text_oid}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Удаление текста по oid",
)
@inject
async def delete_text_by_oid_handler(
    schema: DeleteTextByOidInSchema,
    use_case: FromDishka[DeleteTextByOidUseCase],
) -> None:
    command = DeleteTextByOidCommand(text_oid=schema.oid)

    await use_case.act(command=command)


@router.get(
    path="/all",
    status_code=status.HTTP_200_OK,
    description="Получить все текста",
    response_model=GetAllTextsOutSchema,
)
@inject
async def get_all_texts_handler(
    settings: FromDishka[CommonSettings],
    use_case: FromDishka[GetAllTextsUseCase],
) -> GetAllTextsOutSchema:
    command = GetAllTextCommand(cache_exp=settings.redis.cache_life_time)

    use_case_result: GetAllTextResult = await use_case.act(command=command)

    texts_result: list[TextSchema] = []
    for text in use_case_result.texts:
        content = text.content

        text_result = TextSchema(
            oid=str(text.oid),
            content=content.as_genetic_type(),
        )
        texts_result.append(text_result)

    result = GetAllTextsOutSchema(texts=texts_result)

    return result


@router.get(
    path="/by_count/{count}",
    status_code=status.HTTP_200_OK,
    description="Получить n текстов",
    response_model=GetTextsByCountOutSchema,
)
@inject
async def get_texts_by_count_handler(
    count: int,
    settings: FromDishka[CommonSettings],
    use_case: FromDishka[GetTextsByCountUseCase],
) -> GetTextsByCountOutSchema:
    command = GetTextsByCountCommand(
        count=count,
        cache_exp=settings.redis.cache_life_time,
    )

    use_case_result: GetTextsByCountResult = await use_case.act(command=command)

    texts_result: list[TextSchema] = []
    for text in use_case_result.texts:
        content = text.content

        text_result = TextSchema(
            oid=str(text.oid),
            content=content.as_genetic_type(),
        )
        texts_result.append(text_result)

    result = GetTextsByCountOutSchema(texts=texts_result)

    return result


@router.get(
    path="/{text_oid}",
    status_code=status.HTTP_200_OK,
    description="Получить текст по oid",
    response_model=GetTextByOidOutSchema,
)
@inject
async def get_text_by_oid_handler(
    text_oid: str,
    settings: FromDishka[CommonSettings],
    use_case: FromDishka[GetTextByOidUseCase],
) -> GetTextByOidOutSchema:
    command = GetTextByOidCommand(
        text_oid=text_oid,
        cache_exp=settings.redis.cache_life_time,
    )

    use_case_result: GetTextByOidResult = await use_case.act(command=command)

    content = use_case_result.text.content

    text_result = TextSchema(
        oid=str(use_case_result.text.oid),
        content=content.as_genetic_type(),
    )

    result = GetTextByOidOutSchema(text=text_result)

    return result