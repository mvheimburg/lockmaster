from abc import ABC, abstractmethod
from pathlib import Path
import flet as ft


class AppRoot(ABC):

    @property
    @abstractmethod
    def page(self) -> ft.Page:
        pass

    @property
    @abstractmethod
    def assets(self) -> Path:
        pass

    @abstractmethod
    def change_view(self, view: str):
        pass

    @abstractmethod
    async def ring_bell(self):
        pass

    # @abstractmethod
    # async def show_keypad(self):
    #     pass

    # @abstractmethod
    # async def hide_keypad(self):
    #     pass

    @abstractmethod
    def run_task(self, func):
        pass

    @abstractmethod
    async def validate(self, ce: ft.ControlEvent):
        pass
        # self.page.run_task(func)