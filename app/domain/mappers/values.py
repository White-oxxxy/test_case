from domain.values.text import ContentValue


class TextValuesMapper:
    @staticmethod
    def get_content_value(content: str) -> ContentValue:
        content_value = ContentValue(value=content)
        return content_value