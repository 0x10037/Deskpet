from pygame import image, font
from pygame._sdl2 import Texture
from pathlib import Path
import sys


def resource_path(*parts) -> Path:
    if getattr(sys, "frozen", False):
        base = Path(sys._MEIPASS)
    else:
        base = Path(__file__).parent.parent.parent
    return base.joinpath(*parts)


def user_data_path(*parts) -> Path:
    if getattr(sys, "frozen", False):
        base = Path(sys.executable).parent
    else:
        base = Path(__file__).parent.parent.parent
    return base.joinpath(*parts)


ICON_PATH = resource_path("resources", "icon.ico")


def load_action_images(action, renderer):
    p = resource_path("resources", action)
    return [Texture.from_surface(renderer, image.load(f)) for f in p.glob("*.png")]


def load_all_actions(renderer):
    return {
        "idle": load_action_images("idle", renderer),
        "hanging": load_action_images("hanging", renderer),
    }


def load_font(size=24):
    return font.Font(str(resource_path("resources", "msyh.ttc")), size=size)
