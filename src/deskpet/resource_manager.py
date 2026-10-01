from pygame import image, font
from pygame._sdl2 import Texture
from deskpet.constants import SIZE_DEFAULT, FPS_DEFAULT
from pathlib import Path
import sys


def resource_path(*parts) -> Path:
    """只读资源目录。开发环境在项目根，打包后在 _MEIPASS。"""
    if getattr(sys, "frozen", False):
        base = Path(sys._MEIPASS)
    else:
        base = Path(__file__).parent.parent.parent
    return base.joinpath(*parts)


def user_data_path(*parts) -> Path:
    """可写数据目录。开发环境在项目根，打包后在 exe 旁边。"""
    if getattr(sys, "frozen", False):
        base = Path(sys.executable).parent
    else:
        base = Path(__file__).parent.parent.parent
    return base.joinpath(*parts)


DEFAULT_CONFIG = {"size": SIZE_DEFAULT, "FPS": FPS_DEFAULT}
USER_DATA_DIR = user_data_path()          # 可写目录
ICON_PATH = resource_path("resources", "icon.ico")   # 只读资源


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