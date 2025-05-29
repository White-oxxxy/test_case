from dishka import (
    Provider,
    Scope,
    provide,
)

from domain.mappers import TextEntityMapper
from domain.infra.repositories import ITextRepositoryOrm
from domain.infra.cache import ICacheManager
from domain.logic.services import IAddTextService
from logic.use_cases import (
    AddTextUseCase,
    DeleteTextByOidUseCase,
    GetAllTextsUseCase,
    GetTextsByCountUseCase,
    GetTextByOidUseCase,
)


class UseCasesProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def create_add_text_use_case(
        self,
        text_entity_mapper: TextEntityMapper,
        text_service: IAddTextService
    ) -> AddTextUseCase:
        use_case = AddTextUseCase(
            text_entity_mapper=text_entity_mapper,
            text_service=text_service,
        )
        return use_case

    @provide(scope=Scope.REQUEST)
    def create_delete_text_by_oid_use_case(
        self,
        text_repo: ITextRepositoryOrm,
    ) -> DeleteTextByOidUseCase:
        use_case = DeleteTextByOidUseCase(text_repo=text_repo)
        return use_case

    @provide(scope=Scope.REQUEST)
    def create_get_all_text_use_case(
        self,
        text_repo: ITextRepositoryOrm,
        cache_manager: ICacheManager,
    ) -> GetAllTextsUseCase:
        use_case = GetAllTextsUseCase(
            text_repo=text_repo,
            cache_manager=cache_manager,
        )
        return use_case

    @provide(scope=Scope.REQUEST)
    def create_get_texts_by_count_use_case(
        self,
        text_repo: ITextRepositoryOrm,
        cache_manager: ICacheManager,
    ) -> GetTextsByCountUseCase:
        use_case = GetTextsByCountUseCase(
            text_repo=text_repo,
            cache_manager=cache_manager,
        )
        return use_case

    @provide(scope=Scope.REQUEST)
    def create_get_text_by_oid_use_case(
        self,
        text_repo: ITextRepositoryOrm,
        cache_manager: ICacheManager,
    ) -> GetTextByOidUseCase:
        use_case = GetTextByOidUseCase(
            text_repo=text_repo,
            cache_manager=cache_manager,
        )
        return use_case