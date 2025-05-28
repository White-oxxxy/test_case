from dishka import (
    Provider,
    Scope,
    provide,
)

from domain.mappers import TextEntityMapper
from domain.infra.repositories import ITextRepositoryOrm
from domain.logic.services import IAddTextService
from domain.logic.use_cases import (
    IAddTextUseCase,
    IDeleteTextByOidUseCase,
    IGetAllTextsUseCase,
    IGetTextsByCountUseCase,
    IGetTextByOidUseCase,
)
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
    ) -> IAddTextUseCase:
        use_case = AddTextUseCase(
            text_entity_mapper=text_entity_mapper,
            text_service=text_service,
        )
        return use_case

    @provide(scope=Scope.REQUEST)
    def create_delete_text_by_oid_use_case(
            self,
            text_repo: ITextRepositoryOrm,
    ) -> IDeleteTextByOidUseCase:
        use_case = DeleteTextByOidUseCase(text_repo=text_repo)
        return use_case