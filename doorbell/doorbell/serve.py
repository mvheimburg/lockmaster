from pathlib import Path
from doorbell.app import App, Deploy
import asyncio
from hypercorn.config import Config
# from hypercorn.asyncio import serve

import flet as ft

current_dir=Path().absolute()
print(current_dir)
assets = current_dir / "doorbell" / "assets"
# config = Config.from_toml(current_dir/ "hyper.toml")

bellcount = 1

async def main(page: ft.Page):
    await asyncio.sleep(1)
    app = App(page, assets, bellcount)
    app.run()

ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=5556)


# print(assets)
# t = Deploy(assets=assets)
# # app = t.serve()

# config = Config.from_toml(current_dir/ "hyper.toml")
# # config
# asyncio.run(serve(t.serve, config))