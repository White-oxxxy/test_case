from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class TextAll:
    @property
    def message(self) -> str:
        return "texts:all"


@dataclass(frozen=True)
class TextByCount:
    count: int

    @property
    def message(self) -> str:
        return f"texts:by_count_{self.count}"


@dataclass(frozen=True)
class TextByOid:
    oid: str

    @property
    def message(self) -> str:
        return f"text:by_oid_{self.oid}"