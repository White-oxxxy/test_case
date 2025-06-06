from functools import lru_cache

from dishka import (
    make_async_container,
    AsyncContainer,
)
from dishka.integrations.fastapi import FastapiProvider
from dishka.integrations.taskiq import TaskiqProvider

from di.providers import (
    WriteDatabaseProvider,
    WriteDaosProvider,
    WriteRepositoriesProvider,
    ReadDatabaseProvider,
    ReadDaosProvider,
    ReadRepositoryProvider,
    WriteRedisProvider,
    WriteCacheManagerProvider,
    ReadRedisProvider,
    ReadCacheManagerProvider,
    SettingsProvider,
    DomainMappersProvider,
    InfraMapperProvider,
    ServicesProvider,
    UseCasesProvider,
)


@lru_cache(1)
def get_container() -> AsyncContainer:
    async_container: AsyncContainer = make_async_container(
        FastapiProvider(),
        TaskiqProvider(),
        WriteDatabaseProvider(),
        WriteDaosProvider(),
        WriteRepositoriesProvider(),
        ReadDatabaseProvider(),
        ReadDaosProvider(),
        ReadRepositoryProvider(),
        WriteRedisProvider(),
        WriteCacheManagerProvider(),
        ReadRedisProvider(),
        ReadCacheManagerProvider(),
        SettingsProvider(),
        DomainMappersProvider(),
        InfraMapperProvider(),
        ServicesProvider(),
        UseCasesProvider(),
    )
    return async_container