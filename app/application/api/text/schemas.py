from pydantic import BaseModel


class TextSchema(BaseModel):
    oid: str
    content: str


class CreateTextSchema(BaseModel):
    content: str


class GetAllTextsOutSchema(BaseModel):
    texts: list[TextSchema]


class GetTextByOidOutSchema(BaseModel):
    text: TextSchema


class GetTextsByCountOutSchema(BaseModel):
    texts: list[TextSchema]


class DeleteTextByOidInSchema(BaseModel):
    oid: str


class HealthCheckOutSchema(BaseModel):
    status: str
