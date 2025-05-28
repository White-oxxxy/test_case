from dishka import (
    make_async_container,
    AsyncContainer,
)
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
    return container