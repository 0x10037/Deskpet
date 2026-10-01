# 此文件部分AI生成
import pygame
from deskpet.resource_manager import load_font

pygame.font.init()
font = load_font()


class UIElement:
    def __init__(self, setting, parent, rect):
        self.setting = setting
        self.parent = parent
        self.rect = rect
        self.surface = pygame.Surface((rect.width, rect.height))
        self.visible = True
        self.bind_events()

    def draw(self):
        pass

    def update(self):
        pass

    def bind_events(self):
        pass

    def get_global_rect(self):
        global_rect = self.rect.copy()
        current = self.parent
        while current:
            global_rect.x += current.rect.x
            global_rect.y += current.rect.y
            current = current.parent
        return global_rect

    def is_visible(self):
        """检查自身及所有祖先容器是否可见。"""
        if not self.visible:
            return False
        current = self.parent
        while current is not None:
            if not getattr(current, "visible", True):
                return False
            current = getattr(current, "parent", None)
        return True


class Container(UIElement):
    def __init__(self, setting, parent, rect,
                 direction="vertical", spacing=10, padding=10, bg_color=(255, 255, 255)):
        super().__init__(setting, parent, rect)
        self.direction = direction
        self.spacing = spacing
        self.padding = padding
        self.children = []
        self._next_x = padding
        self._next_y = padding
        self.bg_color = bg_color
        self.choosing = None

    def add_child(self, child, width=None, height=None):
        if width is None:
            width = child.rect.width if child.rect else self.rect.width - self.padding * 2
        if height is None:
            height = child.rect.height if child.rect else 40

        if self.direction == "vertical":
            x = self.padding
            y = self._next_y
            self._next_y += height + self.spacing
        else:
            x = self._next_x
            y = self.padding
            self._next_x += width + self.spacing

        new_rect = pygame.Rect(x, y, width, height)
        child.rect = new_rect
        child.parent = self
        if hasattr(child, "_render_text"):
            # noinspection PyProtectedMember
            child._render_text(width, height)
        else:
            child.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.children.append(child)

    def remove_child(self, child):
        if child in self.children:
            self.children.remove(child)

    def relayout(self):
        self._next_x = self.padding
        self._next_y = self.padding
        for child in self.children:
            w, h = child.rect.width, child.rect.height
            if self.direction == "vertical":
                child.rect.x = self.padding
                child.rect.y = self._next_y
                self._next_y += h + self.spacing
            else:
                child.rect.x = self._next_x
                child.rect.y = self.padding
                self._next_x += w + self.spacing

    def set_choosing(self, child):
        for child_ in self.children:
            child_.choosing = False
        child.choosing = True
        self.choosing = child.text

    def draw(self):
        self.surface.fill(self.bg_color)
        for child in self.children:
            if not child.visible:
                continue
            child.draw()
            self.surface.blit(child.surface, child.rect.topleft)

    def find_button_with_text(self, text):
        for child in self.children:
            if child.text == text:
                return child
        return None


class Button(UIElement):
    def __init__(self, setting, parent, rect, text="Button",
                 bg_color=(100, 150, 200), text_color=(255, 255, 255), bg_color_hover=(255, 0, 0),
                 bg_color_choosing=(0, 0, 255), choosable=True):
        super().__init__(setting, parent, rect)
        self.on_mouse_move = None
        self.on_mouse_down = None
        self.text = text
        self.bg_color = bg_color
        self.bg_color_hover = bg_color_hover
        self.bg_color_choosing = bg_color_choosing
        self.choosing = False
        self.using_bg_color = bg_color
        self.text_color = text_color
        self._on_click = lambda: 0
        self.text_surf = font.render(self.text, True, self.text_color)
        self.choosable = choosable

    def draw(self):
        if self.choosing:
            self.surface.fill(self.bg_color_choosing)
        else:
            self.surface.fill(self.using_bg_color)
        text_rect = self.text_surf.get_rect(center=(self.rect.width // 2, self.rect.height // 2))
        self.surface.blit(self.text_surf, text_rect)

    def on_click(self):
        def inner(func):
            self._on_click = func

        return inner

    def bind_events(self):
        @self.setting.bind(pygame.MOUSEBUTTONDOWN)
        def on_mouse_down(event):
            if not self.is_visible():
                return
            if self.get_global_rect().collidepoint(event.pos):
                self._on_click()
                if self.choosable:
                    self.parent.set_choosing(self)

        @self.setting.bind(pygame.MOUSEMOTION)
        def on_mouse_move(event):
            # 不可见时强制恢复默认色，避免隐藏后残留 hover 效果
            if not self.is_visible():
                self.using_bg_color = self.bg_color
                return
            if self.get_global_rect().collidepoint(event.pos):
                self.using_bg_color = self.bg_color_hover
            else:
                self.using_bg_color = self.bg_color

        self.on_mouse_down = on_mouse_down
        self.on_mouse_move = on_mouse_move

    def __del__(self):
        try:
            self.setting.bindings[pygame.MOUSEBUTTONDOWN].remove(self.on_mouse_down)
            self.setting.bindings[pygame.MOUSEMOTION].remove(self.on_mouse_move)
        except:
            pass


class Slider(UIElement):
    def __init__(self, setting, parent, rect, min_val=0, max_val=100, step=1,
                 default_val=50, bg_color=None, fill_color=(100, 200, 100),
                 handle_color=(50, 50, 50), handle_radius=10, track_color=(0, 0, 0)):
        super().__init__(setting, parent, rect)
        # 使用透明表面
        self.surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        self.min_val = min_val
        self.max_val = max_val
        self.step = step
        self.value = default_val
        self.track_color = track_color
        self.fill_color = fill_color
        self.handle_color = handle_color
        self.handle_radius = handle_radius
        self.track_height = 4  # 轨道/填充线高度
        self.dragging = False
        self.on_change = lambda v: None

        # ---- 预渲染底线（轨道） ----
        self.track_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        self.track_surface.fill((0, 0, 0, 0))
        track_y = rect.height // 2
        pygame.draw.line(self.track_surface, self.track_color,
                         (0, track_y), (rect.width, track_y), 1)

    def draw(self):
        # 清空表面
        self.surface.fill((0, 0, 0, 0))
        # 绘制预渲染的轨道
        self.surface.blit(self.track_surface, (0, 0))

        w = self.rect.width
        h = self.rect.height
        ratio = (self.value - self.min_val) / (self.max_val - self.min_val)
        handle_x = int(ratio * w)
        handle_x = max(0, min(handle_x, w))
        track_y = h // 2

        # 绘制填充线（从起点到滑块位置）
        if handle_x > 0:
            half = self.track_height // 2
            fill_rect = pygame.Rect(0, track_y - half, handle_x, self.track_height)
            pygame.draw.rect(self.surface, self.fill_color, fill_rect)

        # 绘制滑块手柄（圆形）
        pygame.draw.circle(self.surface, self.handle_color,
                           (handle_x, track_y), self.handle_radius)

    def bind_events(self):
        @self.setting.bind(pygame.MOUSEBUTTONDOWN)
        def on_mouse_down(event):
            if not self.is_visible():
                return
            if self.get_global_rect().collidepoint(event.pos):
                self.dragging = True
                self._update_value(event.pos)

        @self.setting.bind(pygame.MOUSEBUTTONUP)
        def on_mouse_up(event):
            if self.dragging:
                self.dragging = False

        @self.setting.bind(pygame.MOUSEMOTION)
        def on_mouse_move(event):
            if self.dragging:
                # 拖动途中父级被隐藏，则取消拖动
                if not self.is_visible():
                    self.dragging = False
                    return
                self._update_value(event.pos)

    def _update_value(self, mouse_pos):
        if not self.is_visible():
            return
        # 判断当前滑块是否属于当前激活的标签页
        top_container = self.parent.parent
        if top_container is None:
            return
        current_tab = self.setting.left_container.choosing
        if not current_tab:
            return
        if self.setting.right_containers.get(current_tab) != top_container:
            return

        local_x = mouse_pos[0] - self.get_global_rect().x
        local_x = max(0, min(local_x, self.rect.width))
        ratio = local_x / self.rect.width
        new_val = self.min_val + ratio * (self.max_val - self.min_val)
        new_val = round(new_val / self.step) * self.step
        new_val = max(self.min_val, min(self.max_val, new_val))
        if new_val != self.value:
            self.value = new_val
            self.on_change(self.value)


# noinspection PyShadowingNames
class Toggle(UIElement):
    def __init__(self, setting, parent, rect, checked=False,
                 bg_color=(200, 200, 200), checked_color=(100, 200, 100),
                 border_color=(50, 50, 50), check_mark_color=(255, 255, 255)):
        super().__init__(setting, parent, rect)
        self.checked = checked
        self.bg_color = bg_color
        self.checked_color = checked_color
        self.border_color = border_color
        self.check_mark_color = check_mark_color
        self.on_toggle = lambda checked: None

    def draw(self):
        color = self.checked_color if self.checked else self.bg_color
        self.surface.fill(color)
        pygame.draw.rect(self.surface, self.border_color, self.surface.get_rect(), 2)
        if self.checked:
            w, h = self.rect.width, self.rect.height
            margin = 4
            points = [(margin, h // 2), (w // 2, h - margin), (w - margin, margin)]
            pygame.draw.lines(self.surface, self.check_mark_color, False, points, 3)

    def bind_events(self):
        @self.setting.bind(pygame.MOUSEBUTTONDOWN)
        def on_mouse_down(event):
            if not self.is_visible():
                return
            if self.get_global_rect().collidepoint(event.pos):
                self.checked = not self.checked
                self.on_toggle(self.checked)


class HBox(Container):
    def __init__(self, setting, parent, rect, spacing=10, padding=5, bg_color=(200, 200, 200)):
        super().__init__(setting, parent, rect,
                         direction="horizontal", spacing=spacing,
                         padding=padding, bg_color=bg_color)

    def add_pair(self, left_widget, right_widget,
                 left_width=None, right_width=None, height=None):
        total_width = self.rect.width - 2 * self.padding
        if left_width is None and right_width is None:
            left_width = (total_width - self.spacing) // 2
            right_width = total_width - self.spacing - left_width
        elif left_width is None:
            left_width = total_width - self.spacing - right_width
        elif right_width is None:
            right_width = total_width - self.spacing - left_width

        height = height or 40
        self.add_child(left_widget, width=left_width, height=height)
        self.add_child(right_widget, width=right_width, height=height)
        return left_widget, right_widget


class Text(UIElement):
    def __init__(self, setting, parent, rect, text="",
                 text_color=(0, 0, 0), bg_color=None, align="center"):
        super().__init__(setting, parent, rect)
        self.bg_color = bg_color
        self._text = text
        self.text_color = text_color
        self.align = align
        self.font = font
        self._render_text()

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if value != self._text:
            self._text = value
            self._render_text()

    def _render_text(self, width=None, height=None):
        if width and height:
            self.rect.width, self.rect.height = width, height
        self.surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        if self.bg_color:
            self.surface.fill(self.bg_color)

        text_surf = self.font.render(self._text, True, self.text_color)
        text_rect = text_surf.get_rect()
        # 对齐计算
        if self.align == "left":
            x = 0
        elif self.align == "right":
            x = self.rect.width - text_rect.width
        else:
            x = (self.rect.width - text_rect.width) // 2
        y = (self.rect.height - text_rect.height) // 2
        self.surface.blit(text_surf, (x, y))
        # self.surface = text_surf


class TextLines(Container):
    def __init__(self, setting, parent, rect, lines=None,
                 spacing=4, padding=8, text_color=(0, 0, 0), bg_color=(255, 255, 255), align="center"):
        # 垂直容器
        super().__init__(setting, parent, rect,
                         direction="vertical", spacing=spacing,
                         padding=padding, bg_color=bg_color)
        self.text_color = text_color
        self._lines = lines or []
        self.align = align
        self._create_children()

    def _create_children(self):
        # 清空原有子项（避免重复添加）
        self.children.clear()
        self._next_y = self.padding
        for line in self._lines:
            # 使用现有全局 font（不修改字体大小）
            text = Text(self.setting, self, pygame.Rect(0, 0, 0, 0),
                        text=line, text_color=self.text_color, align=self.align)
            # 自动计算行高（使用全局 font 的尺寸）
            line_height = font.size(line)[1] + 4  # 加一点间距
            child_width = self.rect.width - 2 * self.padding
            self.add_child(text, width=child_width, height=line_height)
        self.relayout()

    def set_lines(self, new_lines):
        """更新显示的多行文本"""
        self._lines = new_lines
        self._create_children()

    @property
    def lines(self):
        return self._lines

    @lines.setter
    def lines(self, value):
        self.set_lines(value)