from pydantic import BaseModel
from uuid import UUID


class TextSchema(BaseModel):
    oid: UUID
    content: str


class CreateTextSchema(BaseModel):
    content: str


class GetAllTextsOutSchema(BaseModel):
    texts: list[TextSchema]


class GetTextsByOidInSchema(BaseModel):
    oid: UUID


class GetTextByOidOutSchema(BaseModel):
    text: TextSchema


class GetTextsByCountInSchema(BaseModel):
    count: int


class GetTextsByCountOutSchema(BaseModel):
    texts: list[TextSchema]


class DeleteTextByOidInSchema(BaseModel):
    oid: UUID
