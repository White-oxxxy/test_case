from dishka import (
    make_async_container,
    AsyncContainer,
)
from dishka.integrations.fastapi import FastapiProvider
from dishka.integrations.taskiq import TaskiqProvider

from di.providers import (
    DatabaseProvider,
    RedisProvider,
    DaosProvider,
    RepositoriesProvider,
    CacheManagerProvider,
    SettingsProvider,
    DomainMappersProvider,
    InfraMapperProvider,
    ServicesProvider,
    UseCasesProvider,
)


async def get_container() -> AsyncContainer:
    async_container: AsyncContainer = make_async_container(
        FastapiProvider(),
        TaskiqProvider(),
        DatabaseProvider(),
        RedisProvider(),
        DaosProvider(),
        RepositoriesProvider(),
        CacheManagerProvider(),
        SettingsProvider(),
        DomainMappersProvider(),
        InfraMapperProvider(),
        ServicesProvider(),
        UseCasesProvider(),
    )
    return async_container


container: AsyncContainer = make_async_container(
        TaskiqProvider(),
        DatabaseProvider(),
        RedisProvider(),
        DaosProvider(),
        RepositoriesProvider(),
        CacheManagerProvider(),
        SettingsProvider(),
        DomainMappersProvider(),
        InfraMapperProvider(),
        ServicesProvider(),
        UseCasesProvider(),
    )