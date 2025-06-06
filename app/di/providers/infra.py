from typing import (
    Annotated,
    AsyncIterable,
)

from dishka import (
    FromComponent,
    Provider,
    Scope,
    provide,
)
from redis.asyncio import Redis
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)

from core.settings.base import CommonSettings
from domain.infra.daos import (
    ITextWriteDao,
    ITextReadDao,
)
from domain.infra.repositories import (
    ITextWriteRepositoryOrm,
    ITextReadRepositoryOrm,
)
from domain.infra.cache import (
    IWriteCacheManager,
    IReadCacheManager,
)

from infra.redis import (
    WriteCacheManager,
    ReadCacheManager,
)
from infra.pg.dao import (
    TextWriteDao,
    TextReadDao,
)
from infra.pg.repositories import (
    TextWriteRepositoryOrm,
    TextReadRepositoryOrm,
)
from infra.pg.mappers import TextOrmToTextDomainMapper
from infra.monitoring.metrics.custom_metrics import (
    db_query_duration,
    db_success_counter,
    db_error_counter,
    cache_duration,
    cache_success_counter,
    cache_error_counter,
)
from infra.monitoring.instruments.proxies import (
    DaoType,
    CacheManagerType,
)
from infra.monitoring.instruments.fabrics import (
    wrap_dao_with_metrics,
    wrap_cache_manager_with_metrics,
)


class WriteRedisProvider(Provider):
    component = "write_redis"

    @provide(scope=Scope.APP)
    def create_redis(
        self,
        settings: Annotated[CommonSettings, FromComponent("")],
    ) -> Redis:
        redis = Redis(
            host=settings.redis.master_host,
            port=settings.redis.master_port,
        )
        return redis


class ReadRedisProvider(Provider):
    component = "read_redis"

    @provide(scope=Scope.APP)
    def create_redis(
        self,
        settings: Annotated[CommonSettings, FromComponent("")],
    ) -> Redis:
        redis = Redis(
            host=settings.redis.slave_host,
            port=settings.redis.slave_port,
        )
        return redis


class WriteDatabaseProvider(Provider):
    component = "write_db"

    @provide(scope=Scope.APP)
    async def create_engine(
        self,
        settings: Annotated[CommonSettings, FromComponent("")],
    ) -> AsyncEngine:
        return create_async_engine(
            url=settings.pg.write_database_url,
            isolation_level="READ COMMITTED",
            echo=False,
        )

    @provide(scope=Scope.APP)
    async def create_session_maker(
        self,
        engine: AsyncEngine,
    ) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

    @provide(scope=Scope.REQUEST, provides=AsyncSession)
    async def provide_session(
        self,
        sessionmaker: async_sessionmaker[AsyncSession],
    ) -> AsyncIterable[AsyncSession]:
        async with sessionmaker() as session:
            try:
                yield session
            except SQLAlchemyError:
                await session.rollback()


class ReadDatabaseProvider(Provider):
    component = "read_db"

    @provide(scope=Scope.APP)
    async def create_ro_engine(
        self,
        settings: Annotated[CommonSettings, FromComponent("")],
    ) -> AsyncEngine:
        return create_async_engine(
            url=settings.pg.read_database_url,
            isolation_level="AUTOCOMMIT",
            echo=False
        )

    @provide(scope=Scope.APP)
    async def create_session_maker(
        self,
        engine: AsyncEngine,
    ) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

    @provide(scope=Scope.REQUEST, provides=AsyncSession)
    async def provide_session(
            self,
            sessionmaker: async_sessionmaker[AsyncSession],
    ) -> AsyncIterable[AsyncSession]:
        async with sessionmaker() as session:
            try:
                yield session
            except SQLAlchemyError:
                await session.rollback()


class WriteDaosProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def create_text_dao(
        self,
        session: Annotated[AsyncSession, FromComponent("write_db")],
    ) -> ITextWriteDao:
        dao_name = "text_write_dao"

        dao = TextWriteDao(session=session)

        proxy: ITextWriteDao = self._wrap(
            dao=dao,
            name=dao_name,
        )

        return proxy

    @staticmethod
    def _wrap(dao: DaoType, name: str) -> DaoType:
        wrapped_dao: DaoType = wrap_dao_with_metrics(
            dao=dao,
            name=name,
            duration=db_query_duration,
            success_counter=db_success_counter,
            error_counter=db_error_counter,
        )

        return wrapped_dao


class ReadDaosProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def create_text_dao(
            self,
            session: Annotated[AsyncSession, FromComponent("read_db")],
    ) -> ITextReadDao:
        dao_name = "text_read_dao"

        dao = TextReadDao(session=session)

        proxy: ITextReadDao = self._wrap(
            dao=dao,
            name=dao_name,
        )

        return proxy

    @staticmethod
    def _wrap(dao: DaoType, name: str) -> DaoType:
        wrapped_dao: DaoType = wrap_dao_with_metrics(
            dao=dao,
            name=name,
            duration=db_query_duration,
            success_counter=db_success_counter,
            error_counter=db_error_counter,
        )

        return wrapped_dao


class WriteRepositoriesProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def create_text_repository(
        self,
        session: Annotated[AsyncSession, FromComponent("write_db")],
        text_dao: ITextWriteDao,
    ) -> ITextWriteRepositoryOrm:
        repo = TextWriteRepositoryOrm(
            session=session,
            text_dao=text_dao,
        )
        return repo


class ReadRepositoryProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def create_text_repository(
        self,
        session: Annotated[AsyncSession, FromComponent("read_db")],
        text_dao: ITextReadDao,
        orm_to_domain_mapper: TextOrmToTextDomainMapper,
    ) -> ITextReadRepositoryOrm:
        repo = TextReadRepositoryOrm(
            session=session,
            text_dao=text_dao,
            orm_to_domain_mapper=orm_to_domain_mapper,
        )

        return repo


class WriteCacheManagerProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def create_cache_manager(
        self,
        redis: Annotated[Redis, FromComponent("write_redis")],
    ) -> IWriteCacheManager:
        manager_name = "write_redis_manager"

        manager = WriteCacheManager(redis=redis)

        proxy: IWriteCacheManager = self._wrap(
            manager=manager,
            name=manager_name,
        )

        return proxy

    @staticmethod
    def _wrap(manager: CacheManagerType, name: str) -> CacheManagerType:
        wrapped_manager: CacheManagerType = wrap_cache_manager_with_metrics(
            cache_manager=manager,
            name=name,
            duration=cache_duration,
            success_counter=cache_success_counter,
            error_counter=cache_error_counter
        )

        return wrapped_manager


class ReadCacheManagerProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def create_cache_manager(
        self,
        redis: Annotated[Redis, FromComponent("read_redis")],
    ) -> IReadCacheManager:
        manager_name = "read_redis_manager"

        manager = ReadCacheManager(redis=redis)

        proxy: IReadCacheManager = self._wrap(
            manager=manager,
            name=manager_name,
        )

        return proxy

    @staticmethod
    def _wrap(manager: CacheManagerType, name: str) -> CacheManagerType:
        wrapped_manager: CacheManagerType = wrap_cache_manager_with_metrics(
            cache_manager=manager,
            name=name,
            duration=cache_duration,
            success_counter=cache_success_counter,
            error_counter=cache_error_counter
        )

        return wrapped_manager