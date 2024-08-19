from enum import StrEnum, IntEnum, auto

# SCREEN_WIDTH = 800
# SCREEN_HEIGHT = 480

class Size(IntEnum):
    height = 480
    width = 800

class Views(StrEnum):
    HOME = auto()
    LOGIN = auto()

# import flet as ft
# from pages.home import Home
# from pages.login import Login
# from doorbell.app.approot import AppRoot

# class ViewsHandler():

#     def __init__(self, app: AppRoot):
#         self.app = app



#     def get(self, route_ev: ft.RouteChangeEvent):
#         route = route_ev.route
#         if route == '/':
#             print("returning home")
#             return ft.View(
#                 route='/',
#                 controls=[
#                     Home()
#                 ]
#             )
#         elif route == '/login':
#             print("returning login")
#             return ft.View(
#                 route='/login',
#                 controls=[
#                     Login()
#                 ]
#             )
#         else:
#             return ft.View(
#                 route='/unnonw',
#                 controls=[
#                     ft.Text("Inknonw Route")
#                 ]
#             )
