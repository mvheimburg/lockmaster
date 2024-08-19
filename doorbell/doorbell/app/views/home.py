import flet as ft
import asyncio


from doorbell.app.views.myview import MyView
from doorbell.app.const import Views, Size



class Home(MyView):

    def _get_images(self):
        IMAGES = "familie"
        family = self.app.assets / IMAGES
        image_list = list(family.glob("*.png"))
        ret = [f"{IMAGES}/{img.name}" for img in image_list]
        return ret

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.route = Views.HOME
        self.image_list = self._get_images()
        self.current_image = 0
        self.running: bool = False
        self.image = self.next_image()
      
        self.button = ft.IconButton(icon=ft.icons.DOORBELL_ROUNDED, icon_size=80, on_click=self.app.ring_bell)
        self.controls = [self._view()]

    def _view(self):
        # img_control = self.image
        return ft.Container(
                    content=ft.Row([
                        ft.GestureDetector(
                            content=self.image,
                            on_double_tap=self.app.show_keypad,
                            ),
                        ft.Container(
                            content=self.button,
                            alignment=ft.alignment.center,
                            expand=True)
                        ],),
                    padding=0,
                    width=Size.width,
                    height=Size.height)

    def next_image(self) -> ft.Image:
        self.current_image += 1
        if self.current_image > len(self.image_list) - 1:
            self.current_image = 0
        return ft.Image(
                src=self.image_list[self.current_image],
                # width=Size.width/2,
                # height=Size.height,
                fit=ft.ImageFit.FIT_HEIGHT,
            )

    # def start(self):
        # self.app.run_task(self.image_carousel)

#  def open_dlg(e):
#                 page.dialog = dlg
#                 dlg.open = True
#                 page.update()

#             def open_dlg_modal(e):
#                 page.dialog = dlg_modal
#                 dlg_modal.open = True
#                 page.update()


   

    def did_mount(self):
        self.running = True
        # update_weather calls sync requests.get() and time.sleep() and therefore has to be run in a separate thread
        self.app.run_task(self.image_carousel)

    def will_unmount(self):
        self.running = False

    async def image_carousel(self):
        while self.running:
            await asyncio.sleep(60)
            self.image = self.next_image()
            self.view = self._view()
            self.update()
