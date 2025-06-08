from pydantic import BaseModel


class TextSchema(BaseModel):
    oid: str
    content: str


class CreateTextSchema(BaseModel):
    contents: list[str]


class CreateTextOutSchema(BaseModel):
    message: str
    text: list[TextSchema]


class GetAllTextsOutSchema(BaseModel):
    texts: list[TextSchema]


class GetTextByOidOutSchema(BaseModel):
    text: TextSchema


class GetTextsByCountOutSchema(BaseModel):
    texts: list[TextSchema]


class HealthCheckOutSchema(BaseModel):
    status: str
