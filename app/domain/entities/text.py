from dataclasses import dataclass
from typing import Any

from .base import BaseEntity
from domain.values.text import ContentValue


@dataclass(kw_only=True)
class Text(BaseEntity):
    content: ContentValue

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "oid": self.oid,
            "content": self.content,
        }
        return result

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Text":
        return cls(
            oid=data.get("oid"),
            content=data.get("content"),
        )