from dataclasses import dataclass
from uuid import UUID

from sqlalchemy import (
    Result,
    Select,
    select,
)

from .base import BaseDao
from domain.infra.daos import ITextDao
from infra.pg.models import TextOrm


@dataclass
class TextDao(
    BaseDao[TextOrm],
    ITextDao[TextOrm],
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

    async def create(
        self,
        oid: UUID,
        content: str,
    ) -> None:
        text = TextOrm(
            oid=oid,
            content=content,
        )

        self.session.add(text)

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