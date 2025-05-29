from typing import AsyncIterable

from dishka import (
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
from domain.infra.daos import ITextDao
from domain.infra.repositories import ITextRepositoryOrm
from domain.infra.cache import ICacheManager

from infra.redis import CacheManager
from infra.pg.dao import TextDao
from infra.pg.repositories import TextRepositoryOrm
from infra.pg.mappers import TextOrmToTextDomainMapper


class RedisProvider(Provider):
    @provide(scope=Scope.APP)
    def create_redis(
        self,
        settings: CommonSettings,
    ) -> Redis:
        redis = Redis(
            host=settings.redis.host,
            port=settings.redis.port,
        )
        return redis


class DatabaseProvider(Provider):
    @provide(scope=Scope.APP)
    async def create_engine(
        self,
        settings: CommonSettings,
    ) -> AsyncEngine:
        return create_async_engine(
            url=settings.pg.postgres_url,
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


class DaosProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def create_text_dao(
        self,
        session: AsyncSession,
    ) -> ITextDao:
        dao = TextDao(session=session)
        return dao


class RepositoriesProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def create_text__repository(
        self,
        session: AsyncSession,
        text_dao: ITextDao,
        orm_to_domain_mapper: TextOrmToTextDomainMapper,
    ) -> ITextRepositoryOrm:
        repo = TextRepositoryOrm(
            session=session,
            text_dao=text_dao,
            orm_to_domain_mapper=orm_to_domain_mapper,
        )
        return repo


class CacheManagerProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def create_cache_manager(
        self,
        redis: Redis,
    ) -> ICacheManager:
        manager = CacheManager(redis=redis)
        return manager
