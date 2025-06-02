from dishka import (
    Provider,
    Scope,
    provide,
)

from domain.infra.repositories import ITextRepositoryOrm
from domain.logic.services import IAddTextService
from logic.services import AddTextService
from infra.monitoring.metrics.custom_metrics import (
    service_duration,
    service_counter,
    service_success_counter,
    service_error_counter,
)
from infra.monitoring.proxies import ServiceType
from infra.monitoring.fabrics import wrap_service_with_metrics


class ServicesProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def create_add_text_service(
        self,
        text_repo: ITextRepositoryOrm,
    ) -> IAddTextService:
        service_name = "add_text"

        service = AddTextService(text_repo=text_repo)

        proxy : AddTextService = self._wrap(
            service=service,
            name=service_name
        )

        return proxy

    @staticmethod
    def _wrap(service: ServiceType, name: str) -> ServiceType:
        wrapped_use_case: ServiceType = wrap_service_with_metrics(
            service=service,
            name=name,
            duration=service_duration,
            counter=service_counter,
            success_counter=service_success_counter,
            error_counter=service_error_counter,
        )

        return wrapped_use_case