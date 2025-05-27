from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from domain.infra.daos import IBaseDao
from infra.pg.models import BaseOrm


@dataclass
class BaseDao(IBaseDao[BaseOrm]):
    session: AsyncSession

