from dishka import (
    Provider,
    Scope,
    provide,
)

from domain.mappers import (
    TextValuesMapper,
    TextEntityMapper,
)
from infra.pg.mappers import TextOrmToTextDomainMapper


class DomainMappersProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def create_text_value_mapper(self) -> TextValuesMapper:
        mapper = TextValuesMapper()
        return mapper

    @provide(scope=Scope.REQUEST)
    def create_text_entity_mapper(
        self,
        value_mapper: TextValuesMapper
    ) -> TextEntityMapper:
        mapper = TextEntityMapper(value_mapper=value_mapper)
        return mapper


class InfraMapperProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def create_orm_to_domain_mapper(
        self,
        value_mapper: TextValuesMapper
    ) -> TextOrmToTextDomainMapper:
        mapper = TextOrmToTextDomainMapper(value_mapper=value_mapper)
        return mapper