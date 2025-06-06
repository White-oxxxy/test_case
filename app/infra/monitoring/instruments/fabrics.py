from typing import cast

from opentelemetry.sdk.metrics import (
    Histogram,
    Counter,
)

from infra.monitoring.instruments.proxies import (
    UseCaseWithMetricsProxy,
    UseCaseType,
    ServiceWithMetricsProxy,
    ServiceType,
    DaoWithMetricsProxy,
    DaoType,
    CacheManagerWithMetricsProxy,
    CacheManagerType,
)


def wrap_use_case_with_metrics(
    use_case: UseCaseType,
    name: str,
    duration: Histogram,
    counter: Counter,
    success_counter: Counter,
    error_counter: Counter,
) -> UseCaseType:
    wrapped_use_case: UseCaseType = cast(UseCaseType, UseCaseWithMetricsProxy(
        use_case=use_case,
        name=name,
        duration=duration,
        counter=counter,
        success_counter=success_counter,
        error_counter=error_counter,
    ))

    return wrapped_use_case


def wrap_service_with_metrics(
    service: ServiceType,
    name: str,
    duration: Histogram,
    counter: Counter,
    success_counter: Counter,
    error_counter: Counter,
) -> ServiceType:
    wrapped_service: ServiceType = cast(ServiceType, ServiceWithMetricsProxy(
        service=service,
        name=name,
        duration=duration,
        counter=counter,
        success_counter=success_counter,
        error_counter=error_counter,
    ))

    return wrapped_service


def wrap_dao_with_metrics(
    dao: DaoType,
    name: str,
    duration: Histogram,
    success_counter: Counter,
    error_counter: Counter,
) -> DaoType:
    wrapped_dao: DaoType = cast(DaoType, DaoWithMetricsProxy(
        dao=dao,
        name=name,
        duration=duration,
        success_counter=success_counter,
        error_counter=error_counter,
    ))

    return wrapped_dao


def wrap_cache_manager_with_metrics(
    cache_manager: CacheManagerType,
    name: str,
    duration: Histogram,
    success_counter: Counter,
    error_counter: Counter,
) -> CacheManagerType:
    wrapped_cache_manager: CacheManagerType = cast(CacheManagerType, CacheManagerWithMetricsProxy(
        cache_manager=cache_manager,
        name=name,
        duration=duration,
        success_counter=success_counter,
        error_counter=error_counter,
    ))

    return wrapped_cache_manager