from pathlib import Path
import time
from typing import Any
from paho.mqtt.client import MQTTMessage
import flet as ft
from flet import (
    Page,
    colors,
    Theme,
    View,
    Text

)


from doorbell.app.uix.keypad import KeyPad
from doorbell.app.approot import AppRoot
from doorbell.app.const import Views, Size
from doorbell.app.views.home import Home
from doorbell.mqtt.client import MqttClient
from doorbell.mqtt.config import MqttTopics
# url = "https://github.com/mdn/webaudio-examples/blob/main/audio-analyser/viper.mp3?raw=true"
url = "/audio/bell-ringing-05.wav"


class Timer():
    def __init__(self):
        self._start: float = 0.0
        self._end: float = 0.0

    @property
    def time(self) -> float:
        return self._end - self._start

    def start(self):
        self._start = time.time()

    def end(self) -> float:
        self._end = time.time()
        return self.time


class App(AppRoot):
    # _page: ft.Page
    # _assets: Path

    def __init__(self, page: Page, assets: Path, id: int):
        self._id = id
        self._assets = assets
        self._page = page
        self.bellsound = None

        self.home = Home(app=self)
        self.pin_timer = Timer()
        self.views: list[ft.View] = [
            self.home,
            View(
                route=Views.LOGIN,
                controls=[
                    Text("Home")
                ])]
        self.keypad = KeyPad()
        self.keypad_dlg = ft.AlertDialog(
                modal=True,
                # title=ft.Text("Please confirm"),
                content=self.keypad,
                actions=[
                    ft.TextButton("Submit", on_click=self.validate),
                    ft.TextButton("Close", on_click=self.hide_keypad),
                ],
                # opacity=0.5,
                actions_alignment=ft.MainAxisAlignment.END,
                # on_dismiss=lambda e: print("Modal dialog dismissed!"),
            )

        ## MQTT
        self.mqttc = MqttClient()
        self._topics = MqttTopics.load()
        self.mqttc.subscribe_callback(self._topics.garage.state,
                                      self.update_garage)
        self.mqttc.subscribe_callback(self._topics.mode.state,
                                      self.update_mode)
        self.mqttc.subscribe_callback(self._topics.state.state,
                                      self.update_state)
        self.mqttc.subscribe_callback(self._topics.bell.state,
                                      self.update_bell)
        self.mqttc.connect_std_creds()

        

    # def deploy(self):
    #     ft.app(target=self.app, assets_dir=str(self.assets))

    # def serve(self):
    #     return ft.app(target=self.app, assets_dir=str(self.assets), export_asgi_app=True)

    def run(self):
        
        self._page.title = "Doorbell"
        self._page.padding = 0
        self._page.window_width = Size.width
        self._page.window_height = Size.height
        self._page.window_resizable = False
        self._page.theme = Theme(
            font_family="Verdana")
        self._page.theme.page_transitions.windows = "cupertino"
        self._page.fonts = {
            "Pacifico": "/Pacifico-Regular.ttf"
        }
        self._page.bgcolor = colors.BLUE_GREY_200

        # context = ft.GestureDetector(
        #         mouse_cursor=ft.MouseCursor.CONTEXT_MENU,
        #     )
        
        # self.page.add()

        self.change_view(Views.HOME)
        # self.main_page.start()

    @property
    def active_view(self):
        return self.get_view(self._active_view)
  
    @property
    def assets(self):
        return self._assets
 
    @property
    def page(self):
        return self._page

    @active_view.setter
    def active_view(self, view: str):
        print(f"Should set view {view}")
        self.page.views.clear()
        self._active_view = view
        self.page.views.append(self.active_view)
        self.page.update()

    def add_overlay(self, overlay: Any):
        self._page.overlay.append(overlay)
        self._page.update()

    def run_task(self, func):
        self.page.run_task(func)

    def change_view(self, view: str):
        self.active_view = view

    def get_view(self, view: str) -> View:
        v = next(filter(lambda v: v.route == view, self.views), None)
        if v is None:
            raise ValueError("Unknown view")
        return v

    async def ring_bell(self, *args):
        print("Ringing bell")
        bellsound = ft.Audio(src=url,
                            autoplay=True,
                            volume=0.5,
                            balance=0,
                            on_loaded=lambda _: print("Loaded"),)
        self.add_overlay(bellsound)
        await self.mqttc.ring_bell()

    async def show_keypad(self, ce: ft.ControlEvent):
        self.page.dialog = self.keypad_dlg
        self.keypad_dlg.open = True
        # self.controls = [ft.Stack(controls=[self.keypad, self._view()])]
        self.page.update()

    async def hide_keypad(self, ce: ft.ControlEvent):
        self.keypad.clear()
        self.keypad_dlg.open = False
        self.page.update()

    async def validate(self, ce: ft.ControlEvent):
        print(f"Validating pin: {self.keypad.get_pin()}")
        await self.hide_keypad()
        self.page.update()

    def update_garage(self, message: MQTTMessage):
        print(message.payload)

    def garage_open(self):
        self.mqttc.garage_command(GARAGE_COMMAND.OPEN)

    def garage_close(self):
        self.mqttc.garage_command(GARAGE_COMMAND.CLOSE)

    def garage_stop(self):
        self.mqttc.garage_command(GARAGE_COMMAND.STOP)

    def update_mode(self, message: MQTTMessage):
        print(message.payload)

    def update_state(self, message: MQTTMessage):
        print(message.payload)

    def update_bell(self, message: MQTTMessage):
        print(message.payload)


class Deploy():
    def __init__(self, assets: Path):
        self._assets = assets

    def deploy(self):
        app = App(self._assets)
        ft.app(target=app.run, assets_dir=str(self._assets))

    def serve(self):
        app = App(self._assets)
        return ft.app(target=app.run, assets_dir=str(self._assets), export_asgi_app=True)
