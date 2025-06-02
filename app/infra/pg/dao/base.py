from dataclasses import dataclass
from typing import (
    TypeVar,
    Generic,
)

from sqlalchemy.ext.asyncio import AsyncSession

from domain.infra.daos import IBaseDao
from infra.pg.models import BaseOrm


Model = TypeVar("Model", bound=BaseOrm)
Session = TypeVar("Session", bound=AsyncSession)


@dataclass
class BaseDao(
    Generic[Model, Session],
    IBaseDao[Model, Session]
):
    session: Session

