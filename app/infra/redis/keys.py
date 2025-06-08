from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class TextByOid:
    oid: str

    @property
    def message(self) -> str:
        return f"text:by_oid_{self.oid}"