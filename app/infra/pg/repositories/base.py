from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from domain.infra.repositories import IBaseRepositoryOrm
from infra.pg.models import BaseOrm


@dataclass
class BaseRepositoryOrm(IBaseRepositoryOrm):
    session: AsyncSession

    async def commit(self) -> None:
        await self.session.commit()

    async def flush(self) -> None:
        await self.session.flush()

    async def refresh(self, instance: BaseOrm) -> None:
        await self.session.refresh(instance=instance)