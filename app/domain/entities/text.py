from dataclasses import dataclass

from .base import BaseEntity
from domain.values.text import ContentValue


@dataclass(kw_only=True)
class Text(BaseEntity):
    content: ContentValue