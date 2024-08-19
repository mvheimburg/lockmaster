from __future__ import annotations
from enum import StrEnum, auto

from pydantic_settings import BaseSettings
from pydantic import (
    Field,
)
from doorbell.config.common import CommonSettings


class BUILD_TYPE(StrEnum):
    LOCALHOST = auto()
    RELEASE = auto()


class DBSettings(CommonSettings):
    name: str = Field(alias='POSTGRES_DB', default='localhost')
    server: str = Field(alias='POSTGRES_SERVER', default='localhost')
    username: str | None = Field(alias='POSTGRES_USER', default=None)
    password: str | None = Field(alias='POSTGRES_PASSWORD', default=None)

    @property
    def URI(self):
        return f'postgresql://{self.username}:{self.password}@{self.server}/{self.name}'
