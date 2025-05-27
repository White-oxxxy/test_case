from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from infra.pg.models.common.base import BaseOrm
from infra.pg.models.common.mixins import (
    OidPkMixin,
    CreateAtMixin,
)


class TextOrm(
    BaseOrm,
    OidPkMixin,
    CreateAtMixin,
):
    __tablename__ = "texts"

    content: Mapped[str] = mapped_column(nullable=False)



