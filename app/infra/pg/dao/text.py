from dataclasses import dataclass
from uuid import UUID

from sqlalchemy import (
    Result,
    Select,
    select,
)

from .base import (
    BaseDao,
    Session,
)
from domain.infra.daos import (
    ITextReadDao,
    ITextWriteDao,
)
from infra.pg.models import TextOrm


@dataclass
class TextWriteDao(
    BaseDao[TextOrm, Session],
    ITextWriteDao[TextOrm, Session],

):
    async def add_texts(
        self,
        oids: list[UUID],
        contents: list[str],
    ) -> None:
        texts = [
            TextOrm(oid=oid, content=content)
            for oid, content in zip(oids, contents)
        ]

        self.session.add_all(texts)


    async def delete(
        self,
        text_oid: UUID,
    ) -> TextOrm | None:
        stmt: Select[tuple["TextOrm"]] = (
            select(TextOrm)
            .where(TextOrm.oid == text_oid)
        )
        result: Result[tuple["TextOrm"]] = await self.session.execute(stmt)
        text: TextOrm = result.scalar_one_or_none()
        if not text:
            return None

        await self.session.delete(text)

        return text


@dataclass
class TextReadDao(
    BaseDao[TextOrm, Session],
    ITextReadDao[TextOrm, Session],
):
    async def get_by_oid(
        self,
        required_oid: UUID
    ) -> TextOrm | None:
        text: TextOrm | None = await self.session.get(TextOrm, required_oid)

        return text

    async def get_last_n_texts(
        self,
        count: int,
    ) -> list[TextOrm]:
        stmt: Select[tuple["TextOrm"]] = (
            select(TextOrm)
            .order_by(TextOrm.created_at.desc())
            .limit(count)
        )
        result: Result[tuple["TextOrm"]] = await self.session.execute(stmt)
        texts: list["TextOrm"] = list(result.scalars().all())

        return texts

    async def get_all(self) -> list[TextOrm]:
        stmt: Select[tuple["TextOrm"]] = (
            select(TextOrm)
        )
        result: Result[tuple["TextOrm"]] = await self.session.execute(stmt)
        texts: list["TextOrm"] = list(result.scalars().all())

        return texts