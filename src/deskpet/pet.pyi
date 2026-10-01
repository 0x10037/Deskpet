#方便开发
from deskpet.app import DeskPetApp
from pygame._sdl2 import Texture


class Pet:
    app: DeskPetApp
    images: dict[str, list[Texture]]
    velocityY: float
    max_width: float
    max_height: float
    timer: float
    timer_max: float
    display_width: float
    display_height: float
    task_bar_height: float

    def __init__(self, app: DeskPetApp, display_width, display_height, task_bar_height): ...

    def draw(self): ...

    def update_config(self): ...

    def update(self, delta): ...
