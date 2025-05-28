from dataclasses import dataclass

from .values import TextValuesMapper
from domain.entities import Text
from domain.values.text import ContentValue


@dataclass
class TextEntityMapper:
    value_mapper: TextValuesMapper

    def create_text(
        self,
        content: str,
    ) -> Text:
        content_value: ContentValue = self.value_mapper.get_content_value(content=content)
        text = Text(
            content=content_value
        )
        return text