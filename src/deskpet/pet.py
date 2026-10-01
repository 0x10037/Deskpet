from deskpet.resource_manager import load_all_actions
from deskpet.constants import WIDTH, BODY_HEIGHT, ACTION_IDLE_FRAMES
import math


class Pet:
    def __init__(self, app, display_width, display_height, task_bar_height):
        self.app = app
        self.images = load_all_actions(self.app.renderer)
        self.velocityY = 0
        self.max_height = int(display_height - self.app.config['size'] * BODY_HEIGHT - task_bar_height)
        self.max_width = display_width - self.app.config['size'] * WIDTH
        self.timer = 0
        self.timer_max = ACTION_IDLE_FRAMES * self.app.config['action_speed']
        self.display_width = display_width
        self.display_height = display_height
        self.task_bar_height = task_bar_height

    def draw(self):
        if not self.app.dragging and self.app.window.position[1] == self.max_height:
            idx = math.floor(self.timer / self.app.config['action_speed'])
            self.app.renderer.blit(self.images["idle"][idx])
        else:
            self.app.renderer.blit(self.images["hanging"][0])

    def update_config(self):
        self.max_height = int(self.display_height - self.app.config['size'] * BODY_HEIGHT - self.task_bar_height)
        self.max_width = self.display_width - self.app.config['size'] * WIDTH
        self.timer = 0
        self.timer_max = ACTION_IDLE_FRAMES * self.app.config['action_speed']

    def update(self, delta):
        self.timer += delta
        self.timer %= self.timer_max
        if self.app.dragging:
            self.velocityY = 0
            return
        self.velocityY += delta * self.app.config['gravity']
        p = self.app.window.position
        np = max(0, min(self.max_width, p[0])), max(0, min(self.max_height, p[1] + self.velocityY))
        if np[1] == self.max_height:
            self.velocityY = 0
        elif np[1] == 0:
            self.velocityY = 0
        self.app.window.position = np
