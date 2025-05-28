from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)
from pydantic import Field


class PostgresSettings(BaseSettings):
    model_config = SettingsConfigDict(extra="allow")

    name: str = Field(alias="POSTGRES_NAME", default="POSTGRES_NAME")
    user: str = Field(alias="POSTGRES_USER", default="POSTGRES_USER")
    password: str = Field(alias="POSTGRES_PASSWORD", default="POSTGRES_PASSWORD")
    host: str = Field(alias="POSTGRES_HOST", default="POSTGRES_HOST")
    port: str = Field(alias="POSTGRES_PORT", default="POSTGRES_PORT")

    @property
    def postgres_url(self) -> str:
        return rf"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(extra="allow")

    user: str = Field(alias="REDIS_USER", default="REDIS_USER")
    password: str = Field(alias="REDIS_PASSWORD", default="REDIS_PASSWORD")
    host: str = Field(alias="REDIS_HOST", default="localhost")
    port: int = Field(alias="REDIS_PORT", default=6378)
    cache_life_time: int = Field(alias="CACHE_LIFE_TIME", default=600)

    @property
    def redis_url(self) -> str:
        return rf"redis://{self.host}"


class RmqSettings(BaseSettings):
    model_config = SettingsConfigDict(extra="allow")

    username: str = Field(alias="RMQ_USERNAME", default="RMQ_USERNAME")
    password: str = Field(alias="RMQ_PASSWORD", default="RMQ_PASSWORD")
    host: str = Field(alias="RMQ_HOST", default="localhost")
    port: int = Field(alias="RMQ_PORT", default=5672)

    @property
    def rabbit_broker_url(self) -> str:
        return rf"amqp://{self.username}:{self.password}@{self.host}:{self.port}/"



class CommonSettings(BaseSettings):
    pg: PostgresSettings
    redis: RedisSettings
    rmq: RmqSettings