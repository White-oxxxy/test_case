from dataclasses import dataclass
from typing import Generic

from domain.infra.repositories import IBaseRepositoryOrm
from infra.pg.dao import Session
from infra.pg.models import BaseOrm


@dataclass
class BaseRepositoryOrm(
    Generic[Session],
    IBaseRepositoryOrm[Session],
):
    session: Session

    async def commit(self) -> None:
        await self.session.commit()

    async def flush(self) -> None:
        await self.session.flush()

    async def refresh(self, instance: BaseOrm) -> None:
        await self.session.refresh(instance=instance)