import pygame
from deskpet.windows_api import add_tray_icon, set_tray_callback, WM_RBUTTONUP, WM_LBUTTONUP, _menu_handles, \
    setup_tray_context_menu, show_tray_menu, set_taskbar_visible, load_icon_from_file,set_window_icon
from deskpet.resource_manager import ICON_PATH


def generate_context_menu(app):
    set_taskbar_visible(app.handle, False)
    menu_items = [
        ("设置", app.open_main_menu),
        ("退出", lambda: pygame.event.post(pygame.event.Event(pygame.QUIT, window=app.window))),
    ]

    icon_handle = load_icon_from_file(str(ICON_PATH))
    set_window_icon(app.setting.handle, icon_handle)
    add_tray_icon(app.handle, 0, tooltip="DeskPet_MiTsuHo", icon_handle=icon_handle)
    setup_tray_context_menu(app.handle, menu_items)

    @set_tray_callback(app.handle)
    def on_tray_event(hwnd, msg, wparam, lparam):
        if lparam & 0xFFFF == WM_RBUTTONUP:
            menu = _menu_handles.get(hwnd)
            if menu:
                show_tray_menu(hwnd, menu)
        elif lparam & 0xFFFF == WM_LBUTTONUP:
            app.open_main_menu()
