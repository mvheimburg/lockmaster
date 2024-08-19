import flet as ft

from doorbell.app.approot import AppRoot
from doorbell.app.const import Views, Size

class MyView(ft.View):

    def __init__(self, app: AppRoot, **kwargs):
        self.app = app
        super().__init__(padding=0, **kwargs)
