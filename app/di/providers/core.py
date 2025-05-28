from dishka import (
    Provider,
    Scope,
    provide,
)

from core.settings.base import CommonSettings
from core.settings.dev import DevSettings


class SettingsProvider(Provider):
    @provide(scope=Scope.APP)
    def create_settings(self) -> CommonSettings:
        settings: DevSettings = DevSettings()
        return settings