from dishka import (
    Provider,
    Scope,
    provide,
)

from domain.infra.repositories import ITextRepositoryOrm
from domain.logic.services import IAddTextService
from logic.services import AddTextService


class ServicesProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def create_add_text_service(
        self,
        text_repo: ITextRepositoryOrm,
    ) -> IAddTextService:
        service = AddTextService(text_repo=text_repo)
        return service