from dotenv import dotenv_values
from functools import lru_cache
from pathlib import Path

from core.settings.base import (
    CommonSettings,
    PostgresSettings,
    RedisSettings,
    RmqSettings,
)


class DevSettings(CommonSettings):
    def __init__(self, **data):
        env_file = Path(__file__).resolve().parents[3] / ".dev.env"
        env_data = dotenv_values(env_file)

        data["pg"] = PostgresSettings.model_validate(env_data)
        data["redis"] = RedisSettings.model_validate(env_data)
        data["rmq"] = RmqSettings.model_validate(env_data)

        super().__init__(**data)


@lru_cache(1)
def get_settings() -> DevSettings:
    return DevSettings()