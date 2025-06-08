from dataclasses import dataclass
from uuid import UUID

from .base import BaseRepositoryOrm
from domain.entities import Text
from domain.infra.repositories.text import (
    ITextWriteRepositoryOrm,
    ITextReadRepositoryOrm,
)
from domain.infra.daos import (
    ITextWriteDao,
    ITextReadDao,
)
from infra.pg.mappers import TextOrmToTextDomainMapper
from infra.pg.dao import Session
from infra.pg.models import TextOrm
from infra.pg.repositories.exceptions.common import EmptyDataException
from infra.pg.repositories.exceptions.text import TextDoesntExistException


@dataclass
class TextWriteRepositoryOrm(
    BaseRepositoryOrm[Session],
    ITextWriteRepositoryOrm[Session],
):
    text_dao: ITextWriteDao[TextOrm, Session]

    async def add_texts(
        self,
        texts: list[Text],
    ) -> None:
        oids: list[UUID] = []
        contents: list[str] = []
        for text in texts:
            oids.append(text.oid)
            contents.append(text.content.as_genetic_type())

        await self.text_dao.add_texts(
            oids=oids,
            contents=contents,
        )

    async def delete(
        self,
        text_oid: UUID,
    ) -> None:
        text_orm: TextOrm | None = await self.text_dao.delete(text_oid=text_oid)

        if not text_orm:
            raise TextDoesntExistException()


@dataclass
class TextReadRepositoryOrm(
    BaseRepositoryOrm[Session],
    ITextReadRepositoryOrm[Session],
):
    text_dao: ITextReadDao[TextOrm, Session]
    orm_to_domain_mapper: TextOrmToTextDomainMapper

    async def get_by_oid(
        self,
        required_oid: UUID,
    ) -> Text:
        text_orm: TextOrm | None = await self.text_dao.get_by_oid(required_oid=required_oid)

        if text_orm:
            text_entity: Text = self.orm_to_domain_mapper.act(text_orm=text_orm)

            return text_entity

        raise TextDoesntExistException()

    async def get_last_n_texts(
        self,
        count: int,
    ) -> list[Text]:
        text_orms: list[TextOrm] = await self.text_dao.get_last_n_texts(count=count)

        if len(text_orms) > 0:
            text_entities: list[Text] = []
            for text_orm in text_orms:
                text_entity: Text = self.orm_to_domain_mapper.act(text_orm=text_orm)
                text_entities.append(text_entity)

            return text_entities

        raise EmptyDataException()

    async def get_all(self) -> list[Text]:
        text_orms: list[TextOrm] = await self.text_dao.get_all()

        text_entities: list[Text] = []
        for text_orm in text_orms:
            text_entity: Text = self.orm_to_domain_mapper.act(text_orm=text_orm)
            text_entities.append(text_entity)

        return text_entities