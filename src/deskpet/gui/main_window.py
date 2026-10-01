from deskpet.constants import SETTING_HEIGHT, SETTING_WIDTH, SIZE_MIN, SIZE_MAX, FPS_MAX, FPS_MIN, GRAVITY_MAX, \
    GRAVITY_MIN, ACTION_SPEED_MAX, ACTION_SPEED_MIN
from pygame._sdl2 import Window, Renderer
from deskpet.config import DEFAULT_CONFIG
from deskpet.windows_api import get_window_handle_by_title, set_window_focus, set_auto_startup, is_auto_startup_enabled
from deskpet.util import RandomID
from deskpet.gui.controls import Container, Button, Slider, HBox, Text, font, TextLines
from pygame import Rect
from pygame._sdl2 import Texture
from deskpet.constants import VERSION


class Setting:
    def __init__(self, app):
        self.app = app
        ID = f"setting_{RandomID()}"
        self.window = Window(ID, (SETTING_WIDTH, SETTING_HEIGHT), hidden=True)
        self.handle = get_window_handle_by_title(ID)
        self.window.title = "设置"
        self.renderer = Renderer(self.window)
        self.hidden = True
        self.bindings = {}
        buttons = ["桌宠设置", "帧率设置", "开机自启动", "关于"]
        self.left_container = Container(self, None, Rect(0, 0, 160, 360), )
        for button in buttons:
            b = Button(self, self.left_container, Rect(0, 0, 0, 0), button, )
            self.left_container.add_child(b)
        self.right_containers: dict[str, Container] = {k: None for k in buttons}
        self.generate_right_containers()
        self.quit_button = Button(self, None, Rect(500, 254, 140, 44), "保存并退出", choosable=False)

        @self.quit_button.on_click()
        def quit_button_on_click():
            self.save()
            self.hide()

        self.reset_button = Button(self, None, Rect(500, 162, 140, 44), "重置", choosable=False)

        @self.reset_button.on_click()
        def reset_button_on_click():
            c = DEFAULT_CONFIG
            c["first_open"] = False
            self.save(c)
            self.generate_right_containers()

        self.update_button = Button(self, None, Rect(500, 208, 140, 44), "刷新", choosable=False)

        @self.update_button.on_click()
        def update_button_on_click():
            self.save()

        self.exit_app_button = Button(self, None, Rect(500, 300, 140, 44), "关闭程序", choosable=False)

        @self.exit_app_button.on_click()
        def exit_app_button_on_click():
            self.save()
            self.app.exit()

    def generate_right_containers(self):
        config = self.app.config  # 获取当前配置
        right_rect = Rect(160, 0, 480, SETTING_HEIGHT)
        label_kw = {"text_color": (0, 0, 0), "bg_color": None}
        slider_kw = {"bg_color": (200, 200, 200), "fill_color": (100, 200, 100)}
        row_height = font.get_height() + 8

        hbox_padding = 5
        hbox_spacing = 10
        hbox_total_width = right_rect.width - 2 * hbox_padding

        # ---------- 桌宠设置 ----------
        pet_container = Container(self, None, right_rect, bg_color=(240, 240, 255),
                                  spacing=10, padding=10)

        size_val = int(config['size'] * 100)
        grav_val = config['gravity']
        speed_val = int(config['action_speed'] * 100)

        pet_items = [
            ("大小:       ", {
                "min_val": int(SIZE_MIN * 100),
                "max_val": int(SIZE_MAX * 100),
                "default_val": size_val
            }),
            ("重力:       ", {
                "min_val": GRAVITY_MIN,
                "max_val": GRAVITY_MAX,
                "default_val": grav_val
            }),
            ("动画速度:", {
                "min_val": int(ACTION_SPEED_MIN * 100),
                "max_val": int(ACTION_SPEED_MAX * 100),
                "default_val": speed_val
            }),
        ]

        for label_text, slider_params in pet_items:
            label_width = font.size(label_text)[0] + 10
            max_val_str = str(slider_params["max_val"])
            value_width = font.size(max_val_str)[0] + 10
            slider_width = hbox_total_width - label_width - value_width - 2 * hbox_spacing
            if slider_width < 100:
                slider_width = 100

            hbox = HBox(self, pet_container, Rect(0, 0, hbox_total_width, row_height),
                        spacing=hbox_spacing, padding=hbox_padding,
                        bg_color=(240, 240, 255))

            label = Text(self, hbox, Rect(0, 0, 0, 0), label_text, **label_kw)
            slider = Slider(self, hbox, Rect(0, 0, 0, 0), **slider_params, **slider_kw)
            value_text = Text(self, hbox, Rect(0, 0, 0, 0), str(slider_params["default_val"]),
                              text_color=(0, 0, 255), bg_color=None, align="center")

            hbox.add_child(label, width=label_width, height=row_height)
            hbox.add_child(slider, width=slider_width, height=row_height)
            hbox.add_child(value_text, width=value_width, height=row_height)

            def make_callback(text_widget):
                def on_change(val, widget=text_widget):
                    widget.text = str(val)

                return on_change

            slider.on_change = make_callback(value_text)

            pet_container.add_child(hbox, width=hbox_total_width, height=row_height)

        self.right_containers["桌宠设置"] = pet_container

        # ---------- 帧率设置 ----------
        fps_container = Container(self, None, right_rect, bg_color=(240, 255, 240),
                                  spacing=10, padding=10)
        fps_val = config['FPS']
        label_text = "FPS:"
        label_width = font.size(label_text)[0] + 10
        value_width = font.size(str(FPS_MAX))[0] + 10
        slider_width = hbox_total_width - label_width - value_width - 2 * hbox_spacing
        if slider_width < 100:
            slider_width = 100

        hbox_fps = HBox(self, fps_container, Rect(0, 0, hbox_total_width, row_height),
                        spacing=hbox_spacing, padding=hbox_padding,
                        bg_color=(240, 255, 240))
        label_fps = Text(self, hbox_fps, Rect(0, 0, 0, 0), label_text, **label_kw)
        slider_fps = Slider(self, hbox_fps, Rect(0, 0, 0, 0),
                            min_val=FPS_MIN, max_val=FPS_MAX,
                            default_val=fps_val, **slider_kw)
        value_fps = Text(self, hbox_fps, Rect(0, 0, 0, 0), str(fps_val),
                         text_color=(0, 0, 255), bg_color=None, align="center")
        hbox_fps.add_child(label_fps, width=label_width, height=row_height)
        hbox_fps.add_child(slider_fps, width=slider_width, height=row_height)
        hbox_fps.add_child(value_fps, width=value_width, height=row_height)
        slider_fps.on_change = lambda v, w=value_fps: setattr(w, 'text', str(v))
        fps_container.add_child(hbox_fps, width=hbox_total_width, height=row_height)
        self.right_containers["帧率设置"] = fps_container

        # ---------- 关于 ----------
        lines = [
            VERSION,
        ]
        self.right_containers["关于"] = TextLines(self, None, right_rect, lines=lines, bg_color=(240, 240, 255),
                                                  align="left")

        def is_auto_startup_enabled_to_text(auto_startup_enabled):
            if auto_startup_enabled:
                return "开机自启动:开启"
            return "开机自启动:关闭"

        auto_startup_container = Container(self, None, right_rect, bg_color=(240, 240, 255), spacing=10, padding=10)
        is_auto_startup_enabled_text = Text(self, auto_startup_container, Rect(0, 0, 180, 34),
                                            is_auto_startup_enabled_to_text(is_auto_startup_enabled()), **label_kw)
        set_auto_startup_button = Button(self, auto_startup_container, Rect(0, 0, 0, 0), bg_color=(255, 255, 255),
                                         text_color=(0, 0, 0),
                                         choosable=False, text="设置开机自启动")
        auto_startup_container.add_child(is_auto_startup_enabled_text)
        auto_startup_container.add_child(set_auto_startup_button)

        @set_auto_startup_button.on_click()
        def set_auto_startup_button_on_click():
            enabled = not is_auto_startup_enabled()
            set_auto_startup(enabled)
            is_auto_startup_enabled_text.text = is_auto_startup_enabled_to_text(enabled)

        self.right_containers["开机自启动"] = auto_startup_container

    def save(self, config=None):
        if config:
            self.app.config.save(config)
            self.app.update_config()
            return

        label_to_key = {
            "大小": "size",
            "重力": "gravity",
            "动画速度": "action_speed",
            "FPS": "FPS",
        }
        raw = {}

        for container in self.right_containers.values():
            if container is None:
                continue
            for child in container.children:  # child 为 HBox
                if not hasattr(child, 'children'):
                    continue
                label_text = None
                slider = None
                for sub in child.children:
                    if isinstance(sub, Text):
                        txt = sub.text.strip()
                        # 只有包含冒号的才是标签文本
                        if ':' in txt:
                            label_text = txt.replace(':', '').strip()
                    elif isinstance(sub, Slider):
                        slider = sub
                if label_text and slider:
                    key = label_to_key.get(label_text)
                    if key:
                        raw[key] = slider.value

        # 转换单位：大小和动画速度为百分比→比例，其余不变
        final = {}
        for key, val in raw.items():
            if key == "size" or key == "action_speed":
                final[key] = val / 100.0
            else:
                final[key] = val
        final["first_open"] = False
        self.app.config.datas = final
        self.app.config.save()
        self.app.update_config()

    def draw(self):
        self.renderer.draw_color = "#AAAAAA"
        self.renderer.clear()
        self.control_draw(self.left_container)
        for k,v in self.right_containers.items():
            v.visible = False
        choosing = self.left_container.choosing
        if choosing:
            drawing=self.right_containers[choosing]
            drawing.visible = True
            self.control_draw(drawing)
        else:
            k, v = list(self.right_containers.items())[0]
            b = self.left_container.find_button_with_text(k)
            self.left_container.set_choosing(b)
            self.control_draw(v)
        self.control_draw(self.quit_button)
        self.control_draw(self.reset_button)
        self.control_draw(self.update_button)
        self.control_draw(self.exit_app_button)
        self.renderer.present()

    def control_draw(self, control):
        control.draw()
        tex = Texture.from_surface(self.renderer, control.surface)
        self.renderer.blit(tex, control.rect)

    def show(self):
        self.window.show()
        self.hidden = False
        set_window_focus(self.handle)

    def hide(self):
        self.window.hide()
        self.hidden = True

    def bind(self, event):
        def inner(func):
            if self.bindings.get(event):
                self.bindings[event].append(func)
            else:
                self.bindings[event] = [func]

        return inner

    def delete(self):
        self.window.destroy()
