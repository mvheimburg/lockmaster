import flet as ft
from pathlib import Path

def main(page: ft.Page):
    audio1 = ft.Audio(
        src = "/audio/bell-ringing-05.wav",
        # src="https://luan.xyz/files/audio/ambient_c_motion.mp3", 
        autoplay=True
    )
    page.overlay.append(audio1)
    page.update()
    page.add(
        ft.Text("This is an app with background audio."),
        ft.ElevatedButton("Stop playing", on_click=lambda _: audio1.pause()),
    )

current_dir=Path().absolute()
assets = current_dir / "doorbell" / "assets"
ft.app(target=main, assets_dir=assets)