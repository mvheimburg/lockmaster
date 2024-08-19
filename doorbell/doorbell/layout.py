from flet import (
    Control,
    Column,
    Container,
    IconButton,
    Page,
    Row,
    Text,
    IconButton,
    colors,
    icons,
)

class Layout(Row):
    def __init__(
        self,
        app,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.app = app
        self.expand=True
        self.view=0
        # self.views = [CalibrationPage(app=app, assets=self.assets), CalibrationStereoPage(app=app, assets=self.assets), StereoPage(app=app, assets=self.assets)]
        # self.views = [CalibrationStereoPage(app=app), StereoPage(app=app), AiDepthPage(app=app)]
        # self.sidebar = Sidebar(self)
        # self._active_view: Control = self.views[self.view]
        # self.controls = [self.sidebar, self.active_view]
                        #  self.toggle_nav_rail_button, self.active_view]
 
    # @property
    # def active_view(self):
    #     return self._active_view
 
    # @active_view.setter
    # def active_view(self, view):
    #     print(f"Should set view {view}")
    #     if view != self.view:
    #         self._active_view.stop()
    #         self._active_view = self.views[view]
    #         self.controls = [self.sidebar, self.active_view]
    #         self.update()
    #         self.view=view

