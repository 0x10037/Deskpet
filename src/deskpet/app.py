import sys
import pygame
from pygame._sdl2 import Window, Renderer
from deskpet.windows_api import get_window_handle_by_title, set_transparent, set_clickthrough, set_topmost, \
    get_taskbar_height, set_window_focus, create_single_instance_mutex,show_message_box,set_auto_startup,MB_YESNO,MB_TOPMOST,MB_SETFOREGROUND,IDYES,MB_OK
from deskpet.config import Config
from deskpet.util import RandomID
from deskpet.pet import Pet
from deskpet.constants import WIDTH, HEIGHT, APP_NAME
from deskpet.gui.context_menu import generate_context_menu
from deskpet.gui.main_window import Setting

pygame.display.init()
DISPLAY_WIDTH, DISPLAY_HEIGHT = pygame.display.get_desktop_sizes()[0]
TASKBAR_HEIGHT = get_taskbar_height()


class DeskPetApp:
    def __init__(self, config=Config(), have_mutex=False):
        if not have_mutex:
            mutex = create_single_instance_mutex(APP_NAME)
            if mutex is None:
                show_message_box(None,"应用已打开","提示",MB_OK|MB_TOPMOST|MB_SETFOREGROUND)
                self.exit()
        if config["first_open"] is True:
            r = show_message_box(None,"是否开机自启动","开机自启动设置",MB_YESNO|MB_TOPMOST|MB_SETFOREGROUND) == IDYES
            if r:
                set_auto_startup(True)
            config["first_open"] = False
            config.save()
        self.config = config
        self.setting = Setting(self)
        size = self.config['size']
        ID = f"DeskPet_{RandomID()}"
        self.window = Window(ID, (size * WIDTH, size * HEIGHT), hidden=True, always_on_top=True, borderless=True)
        self.renderer = Renderer(self.window)
        self.dragging = False
        self.mouse_pos = (0, 0)
        self.running = False
        self.clock = pygame.time.Clock()
        self.handle = get_window_handle_by_title(ID)
        set_topmost(self.handle, True)
        set_transparent(self.handle, 0x00EFCDAB)
        set_clickthrough(self.handle, False)
        self.pet = Pet(self, DISPLAY_WIDTH, DISPLAY_HEIGHT, TASKBAR_HEIGHT)
        self.delta = 0
        generate_context_menu(self)


    def open_main_menu(self):
        self.setting.show()

    def update_config(self):
        new_size = self.config['size']
        new_width = int(new_size * WIDTH)
        new_height = int(new_size * HEIGHT)
        self.pet.update_config()
        if self.window.size != (new_width, new_height):
            self.window.size = (new_width, new_height)

    def exit(self):
        self.running = False
        pygame.quit()
        sys.exit()

    def update(self):
        self.pet.update(self.delta)

    def get_mouse_true_pos(self):
        return pygame.mouse.get_pos()[0] + self.window.position[0], pygame.mouse.get_pos()[1] + self.window.position[1]

    def move(self, pos):
        self.window.position = pos

    def draw(self):
        self.renderer.draw_color = "#ABCDEFFF"
        self.renderer.clear()
        self.pet.draw()
        self.renderer.present()
        if not self.setting.hidden:
            self.setting.draw()

    def run(self):
        self.draw()
        self.window.show()
        self.running = True
        while self.running:
            for event in pygame.event.get():
                w = event.dict.get("window", self.window)
                if w == self.window:
                    if event.type == pygame.QUIT:
                        self.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        self.mouse_pos = self.get_mouse_true_pos()
                        self.dragging = True
                    elif event.type == pygame.MOUSEBUTTONUP:
                        self.dragging = False
                    elif event.type == pygame.MOUSEMOTION:
                        set_window_focus(self.handle)
                        if self.dragging:
                            p = self.window.position
                            new_mouse_pos = self.get_mouse_true_pos()
                            delta = (new_mouse_pos[0] - self.mouse_pos[0], new_mouse_pos[1] - self.mouse_pos[1])
                            p2 = (p[0] + delta[0], p[1] + delta[1])
                            self.window.position = p2
                            self.mouse_pos = new_mouse_pos
                elif w == self.setting.window:
                    if event.type == pygame.WINDOWCLOSE:
                        self.setting.hide()
                    else:
                        if self.setting.bindings.get(event.type):
                            for binding in self.setting.bindings[event.type]:
                                binding(event)

            self.update()
            self.draw()
            self.delta = self.clock.tick(self.config['FPS']) / 1000
