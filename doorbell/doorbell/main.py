from pathlib import Path
from doorbell.app import App
import asyncio

def main():
    current_dir=Path().absolute()
    print(current_dir)
    assets = current_dir / "doorbell" / "assets"
    print(assets)
    t = App(assets=assets)
    t.deploy()


if __name__ == "__main__":
    main()
