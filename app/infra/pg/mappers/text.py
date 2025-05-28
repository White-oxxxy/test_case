from dataclasses import dataclass

from domain.entities import Text
from domain.values.text import ContentValue
from domain.mappers.values import TextValuesMapper
from infra.pg.models import TextOrm


@dataclass
class TextOrmToTextDomainMapper:
    value_mapper: TextValuesMapper

    def act(
        self,
        text_orm: TextOrm
    ) -> Text:
        content_value: ContentValue = self.value_mapper.get_content_value(content=text_orm.content)
        text_entity = Text(
            oid=text_orm.oid,
            content=content_value,
        )
        return text_entity