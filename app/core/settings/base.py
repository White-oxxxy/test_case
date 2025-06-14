from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)
from pydantic import Field


class PostgresSettings(BaseSettings):
    model_config = SettingsConfigDict(extra="allow")

    name: str = Field(alias="POSTGRES_DB", default="POSTGRES_DB")
    user: str = Field(alias="POSTGRES_USER", default="POSTGRES_USER")
    password: str = Field(alias="POSTGRES_PASSWORD", default="POSTGRES_PASSWORD")
    pgbouncer_host: str = Field(alias="PGBOUNCER_HOST", default="pgbouncer")
    pgbouncer_port: int = Field(alias="PGBOUNCER_PORT", default=6432)

    @property
    def write_database_url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.pgbouncer_host}:{self.pgbouncer_port}/write_db"

    @property
    def read_database_url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.pgbouncer_host}:{self.pgbouncer_port}/read_db"

    @property
    def migration_url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@localhost:45432/text"


class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(extra="allow")

    user: str = Field(alias="REDIS_USER", default="REDIS_USER")
    password: str = Field(alias="REDIS_PASSWORD", default="REDIS_PASSWORD")
    master_host: str = Field(alias="REDIS_MASTER_HOST", default="localhost")
    slave_host: str = Field(alias="REDIS_SLAVE_HOST", default="localhost")
    master_port: int = Field(alias="REDIS_MASTER_PORT", default=6379)
    slave_port: int = Field(alias="REDIS_SLAVE_PORT", default=6379)
    cache_life_time: int = Field(alias="REDIS_CACHE_LIFE_TIME", default=600)


class RmqSettings(BaseSettings):
    model_config = SettingsConfigDict(extra="allow")

    username: str = Field(alias="RMQ_USERNAME", default="RMQ_USERNAME")
    password: str = Field(alias="RMQ_PASSWORD", default="RMQ_PASSWORD")
    host: str = Field(alias="RMQ_HOST", default="localhost")
    port: int = Field(alias="RMQ_PORT", default=5672)

    @property
    def rabbit_broker_url(self) -> str:
        return rf"amqp://{self.username}:{self.password}@{self.host}:{self.port}/"


class OtlpSettings(BaseSettings):
    model_config = SettingsConfigDict(extra="allow")

    host: str = Field(alias="OTLP_HOST", default="localhost")
    port: int = Field(alias="OTLP_PORT", default="4317")

    @property
    def otlp_url(self) -> str:
        return rf"http://{self.host}:{self.port}"


class CommonSettings(BaseSettings):
    pg: PostgresSettings
    redis: RedisSettings
    rmq: RmqSettings
    otlp: OtlpSettings