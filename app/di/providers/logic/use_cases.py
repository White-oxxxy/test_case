from dishka import (
    Provider,
    Scope,
    provide,
)

from domain.mappers import TextEntityMapper
from domain.infra.repositories import (
    ITextWriteRepositoryOrm,
    ITextReadRepositoryOrm,
)
from domain.infra.cache import (
    IWriteCacheManager,
    IReadCacheManager,
)
from domain.logic.services import IAddTextService
from infra.monitoring.metrics.custom_metrics import (
    use_case_duration,
    use_case_counter,
    use_case_success_counter,
    use_case_error_counter,
)
from infra.monitoring.instruments.proxies import UseCaseType
from infra.monitoring.instruments.fabrics import wrap_use_case_with_metrics
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
        use_case_name = "add_text"

        use_case = AddTextUseCase(
            text_entity_mapper=text_entity_mapper,
            text_service=text_service,
        )

        proxy: AddTextUseCase = self._wrap(
            use_case=use_case,
            name=use_case_name,
        )

        return proxy

    @provide(scope=Scope.REQUEST)
    def create_delete_text_by_oid_use_case(
        self,
        text_repo: ITextWriteRepositoryOrm,
    ) -> DeleteTextByOidUseCase:
        use_case_name = "delete_by_oid"

        use_case = DeleteTextByOidUseCase(text_repo=text_repo)

        proxy: DeleteTextByOidUseCase = self._wrap(
            use_case=use_case,
            name=use_case_name,
        )

        return proxy

    @provide(scope=Scope.REQUEST)
    def create_get_all_text_use_case(
        self,
        text_repo: ITextReadRepositoryOrm,
        write_cache_manager: IWriteCacheManager,
        read_cache_manager: IReadCacheManager,
    ) -> GetAllTextsUseCase:
        use_case_name = "get_all_texts"

        use_case = GetAllTextsUseCase(
            text_repo=text_repo,
            write_cache_manager=write_cache_manager,
            read_cache_manager=read_cache_manager,
        )

        proxy: GetAllTextsUseCase = self._wrap(
            use_case=use_case,
            name=use_case_name,
        )

        return proxy

    @provide(scope=Scope.REQUEST)
    def create_get_texts_by_count_use_case(
        self,
        text_repo: ITextReadRepositoryOrm,
        write_cache_manager: IWriteCacheManager,
        read_cache_manager: IReadCacheManager,
    ) -> GetTextsByCountUseCase:
        use_case_name = "get_texts_by_count"

        use_case = GetTextsByCountUseCase(
            text_repo=text_repo,
            write_cache_manager=write_cache_manager,
            read_cache_manager=read_cache_manager,
        )

        proxy: GetTextsByCountUseCase = self._wrap(
            use_case=use_case,
            name=use_case_name,
        )

        return proxy

    @provide(scope=Scope.REQUEST)
    def create_get_text_by_oid_use_case(
        self,
        text_repo: ITextReadRepositoryOrm,
        write_cache_manager: IWriteCacheManager,
        read_cache_manager: IReadCacheManager,
    ) -> GetTextByOidUseCase:
        use_case_name = "get_text_by_oid"

        use_case = GetTextByOidUseCase(
            text_repo=text_repo,
            write_cache_manager=write_cache_manager,
            read_cache_manager=read_cache_manager,
        )

        proxy: GetTextByOidUseCase = self._wrap(
            use_case=use_case,
            name=use_case_name,
        )

        return proxy

    @staticmethod
    def _wrap(use_case: UseCaseType, name: str) -> UseCaseType:
        wrapped_use_case: UseCaseType = wrap_use_case_with_metrics(
            use_case=use_case,
            name=name,
            duration=use_case_duration,
            counter=use_case_counter,
            success_counter=use_case_success_counter,
            error_counter=use_case_error_counter,
        )

        return wrapped_use_case