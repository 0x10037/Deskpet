# AI生成

import ctypes
import sys
import atexit
import winreg  # 用于开机自启动
from ctypes import wintypes

if sys.platform == "win32":
    user32 = ctypes.windll.user32
    kernel32 = ctypes.windll.kernel32
    shell32 = ctypes.windll.shell32

    # ---------- 常量 ----------
    WM_LBUTTONUP = 0x0202
    WM_RBUTTONUP = 0x0205
    WM_MBUTTONUP = 0x0208

    WS_EX_LAYERED = 0x80000
    WS_EX_TRANSPARENT = 0x20
    WS_EX_TOPMOST = 0x8
    WS_EX_TOOLWINDOW = 0x00000080  # 隐藏任务栏按钮
    GWL_EXSTYLE = -20
    LWA_COLORKEY = 0x1
    LWA_ALPHA = 0x2

    SPI_GETWORKAREA = 0x0030
    SM_CYSCREEN = 1

    VK_LBUTTON = 0x01
    VK_RBUTTON = 0x02
    VK_MBUTTON = 0x04

    ERROR_ALREADY_EXISTS = 183

    # 托盘图标相关
    NIM_ADD = 0x00000000
    NIM_MODIFY = 0x00000001
    NIM_DELETE = 0x00000002
    NIF_MESSAGE = 0x00000001
    NIF_ICON = 0x00000002
    NIF_TIP = 0x00000004
    WM_USER = 0x0400
    WM_TRAYICON = WM_USER + 1
    WM_COMMAND = 0x0111
    IDI_APPLICATION = 32512

    GWLP_WNDPROC = -4
    GWL_WNDPROC = -4

    # 菜单常量
    MF_STRING = 0x00000000
    MF_SEPARATOR = 0x00000800
    TPM_LEFTALIGN = 0x0000
    TPM_RIGHTBUTTON = 0x0002

    # 图标加载常量
    IMAGE_ICON = 1
    LR_LOADFROMFILE = 0x00000010
    WM_SETICON = 0x0080
    ICON_SMALL = 0
    ICON_BIG = 1

    # ---------- 新增：消息框常量 ----------
    MB_OK = 0x00000000
    MB_OKCANCEL = 0x00000001
    MB_ABORTRETRYIGNORE = 0x00000002
    MB_YESNOCANCEL = 0x00000003
    MB_YESNO = 0x00000004
    MB_RETRYCANCEL = 0x00000005
    MB_ICONHAND = 0x00000010
    MB_ICONERROR = 0x00000010
    MB_ICONSTOP = 0x00000010
    MB_ICONQUESTION = 0x00000020
    MB_ICONEXCLAMATION = 0x00000030
    MB_ICONWARNING = 0x00000030
    MB_ICONINFORMATION = 0x00000040
    MB_ICONASTERISK = 0x00000040
    MB_DEFBUTTON1 = 0x00000000
    MB_DEFBUTTON2 = 0x00000100
    MB_DEFBUTTON3 = 0x00000200
    MB_DEFBUTTON4 = 0x00000300
    MB_SETFOREGROUND = 0x00010000
    MB_TOPMOST = 0x00040000

    IDOK = 1
    IDCANCEL = 2
    IDABORT = 3
    IDRETRY = 4
    IDIGNORE = 5
    IDYES = 6
    IDNO = 7
    # ---------- 消息框常量结束 ----------

    # ---------- 结构体 ----------
    class RECT(ctypes.Structure):
        _fields_ = [
            ("left", wintypes.LONG),
            ("top", wintypes.LONG),
            ("right", wintypes.LONG),
            ("bottom", wintypes.LONG),
        ]

    class NOTIFYICONDATAW(ctypes.Structure):
        _fields_ = [
            ("cbSize", wintypes.DWORD),
            ("hWnd", wintypes.HWND),
            ("uID", wintypes.UINT),
            ("uFlags", wintypes.UINT),
            ("uCallbackMessage", wintypes.UINT),
            ("hIcon", wintypes.HANDLE),
            ("szTip", wintypes.WCHAR * 128),
            ("dwState", wintypes.DWORD),
            ("dwStateMask", wintypes.DWORD),
            ("szInfo", wintypes.WCHAR * 256),
            ("uTimeout", wintypes.UINT),
            ("szInfoTitle", wintypes.WCHAR * 64),
            ("dwInfoFlags", wintypes.DWORD),
            ("guidItem", ctypes.c_byte * 16),
            ("hBalloonIcon", wintypes.HANDLE),
        ]

    class POINT(ctypes.Structure):
        _fields_ = [("x", wintypes.LONG), ("y", wintypes.LONG)]

    # ---------- 函数声明 ----------
    SetWindowLongW = user32.SetWindowLongW
    SetWindowLongW.argtypes = [wintypes.HWND, ctypes.c_int, ctypes.c_long]
    SetWindowLongW.restype = wintypes.LONG

    GetWindowLongW = user32.GetWindowLongW
    GetWindowLongW.argtypes = [wintypes.HWND, ctypes.c_int]
    GetWindowLongW.restype = wintypes.LONG

    SetLayeredWindowAttributes = user32.SetLayeredWindowAttributes
    SetLayeredWindowAttributes.argtypes = [wintypes.HWND, wintypes.COLORREF, ctypes.c_byte, ctypes.c_ulong]
    SetLayeredWindowAttributes.restype = wintypes.BOOL

    ShowWindow = user32.ShowWindow
    ShowWindow.argtypes = [wintypes.HWND, ctypes.c_int]
    ShowWindow.restype = wintypes.BOOL

    SetForegroundWindow = user32.SetForegroundWindow
    SetForegroundWindow.argtypes = [wintypes.HWND]
    SetForegroundWindow.restype = wintypes.BOOL

    SetFocus = user32.SetFocus
    SetFocus.argtypes = [wintypes.HWND]
    SetFocus.restype = wintypes.HWND

    LoadIconW = user32.LoadIconW
    LoadIconW.argtypes = [wintypes.HINSTANCE, ctypes.c_void_p]
    LoadIconW.restype = wintypes.HANDLE

    LoadImageW = user32.LoadImageW
    LoadImageW.argtypes = [wintypes.HINSTANCE, wintypes.LPCWSTR, wintypes.UINT,
                           ctypes.c_int, ctypes.c_int, wintypes.UINT]
    LoadImageW.restype = wintypes.HANDLE

    SendMessageW = user32.SendMessageW
    SendMessageW.argtypes = [wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM]
    SendMessageW.restype = wintypes.LPARAM

    CreateMutexW = kernel32.CreateMutexW
    CreateMutexW.argtypes = [wintypes.LPVOID, wintypes.BOOL, wintypes.LPCWSTR]
    CreateMutexW.restype = wintypes.HANDLE

    CloseHandle = kernel32.CloseHandle
    CloseHandle.argtypes = [wintypes.HANDLE]
    CloseHandle.restype = wintypes.BOOL

    GetLastError = kernel32.GetLastError
    GetLastError.argtypes = []
    GetLastError.restype = wintypes.DWORD

    Shell_NotifyIconW = shell32.Shell_NotifyIconW
    Shell_NotifyIconW.argtypes = [wintypes.DWORD, ctypes.POINTER(NOTIFYICONDATAW)]
    Shell_NotifyIconW.restype = wintypes.BOOL

    DefWindowProcW = user32.DefWindowProcW
    DefWindowProcW.argtypes = [wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM]
    DefWindowProcW.restype = ctypes.c_int

    # 菜单 API
    CreatePopupMenu = user32.CreatePopupMenu
    CreatePopupMenu.argtypes = []
    CreatePopupMenu.restype = wintypes.HANDLE

    AppendMenuW = user32.AppendMenuW
    AppendMenuW.argtypes = [wintypes.HANDLE, wintypes.UINT, ctypes.c_void_p, wintypes.LPCWSTR]
    AppendMenuW.restype = wintypes.BOOL

    TrackPopupMenu = user32.TrackPopupMenu
    TrackPopupMenu.argtypes = [wintypes.HANDLE, wintypes.UINT, ctypes.c_int, ctypes.c_int,
                               ctypes.c_int, wintypes.HWND, wintypes.LPARAM]
    TrackPopupMenu.restype = wintypes.BOOL

    DestroyMenu = user32.DestroyMenu
    DestroyMenu.argtypes = [wintypes.HANDLE]
    DestroyMenu.restype = wintypes.BOOL

    GetCursorPos = user32.GetCursorPos
    GetCursorPos.argtypes = [ctypes.POINTER(POINT)]
    GetCursorPos.restype = wintypes.BOOL

    # ---------- 新增：声明 MessageBoxW ----------
    user32.MessageBoxW.argtypes = [wintypes.HWND, wintypes.LPCWSTR, wintypes.LPCWSTR, wintypes.UINT]
    user32.MessageBoxW.restype = ctypes.c_int

    # ---------- 基础窗口函数 ----------
    def get_window_handle_by_title(title):
        return user32.FindWindowW(None, title)

    def set_transparent(hwnd, color_key=0x000000):
        exstyle = GetWindowLongW(hwnd, GWL_EXSTYLE)
        SetWindowLongW(hwnd, GWL_EXSTYLE, exstyle | WS_EX_LAYERED)
        SetLayeredWindowAttributes(hwnd, color_key, 0, LWA_COLORKEY)

    def set_clickthrough(hwnd, enable=True):
        exstyle = GetWindowLongW(hwnd, GWL_EXSTYLE)
        if enable:
            SetWindowLongW(hwnd, GWL_EXSTYLE, exstyle | WS_EX_TRANSPARENT)
        else:
            SetWindowLongW(hwnd, GWL_EXSTYLE, exstyle & ~WS_EX_TRANSPARENT)

    def set_topmost(hwnd, enable=True):
        exstyle = GetWindowLongW(hwnd, GWL_EXSTYLE)
        if enable:
            SetWindowLongW(hwnd, GWL_EXSTYLE, exstyle | WS_EX_TOPMOST)
        else:
            SetWindowLongW(hwnd, GWL_EXSTYLE, exstyle & ~WS_EX_TOPMOST)

    def set_taskbar_visible(hwnd, visible=True):
        """控制窗口是否在任务栏显示（visible=False 则隐藏任务栏按钮）"""
        exstyle = GetWindowLongW(hwnd, GWL_EXSTYLE)
        if visible:
            exstyle &= ~WS_EX_TOOLWINDOW
        else:
            exstyle |= WS_EX_TOOLWINDOW
        SetWindowLongW(hwnd, GWL_EXSTYLE, exstyle)

    def get_taskbar_height():
        screen_height = user32.GetSystemMetrics(SM_CYSCREEN)
        work_area = RECT()
        if user32.SystemParametersInfoW(SPI_GETWORKAREA, 0, ctypes.byref(work_area), 0):
            work_height = work_area.bottom - work_area.top
            return screen_height - work_height
        return None

    def set_window_focus(hwnd):
        if hwnd:
            return bool(SetForegroundWindow(hwnd))
        return False

    # ---------- 新增：消息框函数 ----------
    def show_message_box(hwnd, text, caption, style=MB_OK):
        """显示消息框，返回用户选择的按钮ID"""
        return user32.MessageBoxW(hwnd, text, caption, style)

    # ---------- 图标加载与设置 ----------
    def load_icon_from_file(filepath):
        """从 .ico 文件加载图标，返回 HICON 句柄"""
        return LoadImageW(None, filepath, IMAGE_ICON, 0, 0, LR_LOADFROMFILE)

    def set_window_icon(hwnd, icon_handle):
        """设置窗口图标（标题栏和任务栏）"""
        if hwnd and icon_handle:
            SendMessageW(hwnd, WM_SETICON, ICON_SMALL, icon_handle)
            SendMessageW(hwnd, WM_SETICON, ICON_BIG, icon_handle)
            return True
        return False

    # ---------- 单实例互斥 ----------
    def create_single_instance_mutex(name: str):
        mutex = CreateMutexW(None, False, name)
        if not mutex:
            return None
        last_error = GetLastError()
        if last_error == ERROR_ALREADY_EXISTS:
            CloseHandle(mutex)
            return None
        atexit.register(lambda: CloseHandle(mutex))
        return mutex

    # ---------- 托盘图标 ----------
    def add_tray_icon(hwnd, icon_id, tooltip="", icon_handle=None):
        nid = NOTIFYICONDATAW()
        nid.cbSize = ctypes.sizeof(NOTIFYICONDATAW)
        nid.hWnd = hwnd
        nid.uID = icon_id
        nid.uFlags = NIF_MESSAGE | NIF_ICON | NIF_TIP
        nid.uCallbackMessage = WM_TRAYICON
        if icon_handle is not None:
            nid.hIcon = icon_handle
        else:
            nid.hIcon = LoadIconW(None, ctypes.c_void_p(IDI_APPLICATION))
        nid.szTip = tooltip[:127] if tooltip else ""
        return bool(Shell_NotifyIconW(NIM_ADD, ctypes.byref(nid)))

    def remove_tray_icon(hwnd, icon_id):
        nid = NOTIFYICONDATAW()
        nid.cbSize = ctypes.sizeof(NOTIFYICONDATAW)
        nid.hWnd = hwnd
        nid.uID = icon_id
        return bool(Shell_NotifyIconW(NIM_DELETE, ctypes.byref(nid)))

    # ---------- 托盘回调（子类化窗口过程） ----------
    _tray_old_proc = {}
    _tray_callbacks = {}
    _menu_callbacks = {}
    _menu_handles = {}

    WNDPROC = ctypes.WINFUNCTYPE(ctypes.c_int, wintypes.HWND, wintypes.UINT,
                                 wintypes.WPARAM, wintypes.LPARAM)

    def _tray_wndproc(hwnd, msg, wparam, lparam):
        if msg == WM_TRAYICON:
            callback = _tray_callbacks.get(hwnd)
            if callback:
                callback(hwnd, msg, wparam, lparam)
        elif msg == WM_COMMAND:
            menu_id = wparam & 0xFFFF
            cb = _menu_callbacks.get(menu_id)
            if cb:
                cb()
            return 0
        old_proc = _tray_old_proc.get(hwnd)
        if old_proc:
            return old_proc(hwnd, msg, wparam, lparam)
        return DefWindowProcW(hwnd, msg, wparam, lparam)

    _tray_wndproc_cb = WNDPROC(_tray_wndproc)

    def _bind_tray_callback(hwnd, callback):
        if not hwnd or not callable(callback):
            return False

        if hwnd in _tray_old_proc:
            _tray_callbacks[hwnd] = callback
            return True

        try:
            SetWindowLongPtrW = user32.SetWindowLongPtrW
            SetWindowLongPtrW.argtypes = [wintypes.HWND, ctypes.c_int, ctypes.c_longlong]
            SetWindowLongPtrW.restype = ctypes.c_longlong
            old_proc_ptr = SetWindowLongPtrW(hwnd, GWLP_WNDPROC,
                                             ctypes.cast(_tray_wndproc_cb, ctypes.c_void_p).value)
        except AttributeError:
            old_proc_ptr = SetWindowLongW(hwnd, GWL_WNDPROC,
                                          ctypes.cast(_tray_wndproc_cb, ctypes.c_void_p).value)

        if not old_proc_ptr:
            return False

        _tray_old_proc[hwnd] = WNDPROC(old_proc_ptr)
        _tray_callbacks[hwnd] = callback
        return True

    def set_tray_callback(hwnd, callback=None):
        if callback is None:
            def decorator(func):
                _bind_tray_callback(hwnd, func)
                return func

            return decorator
        else:
            return _bind_tray_callback(hwnd, callback)

    def remove_tray_callback(hwnd):
        if hwnd in _tray_old_proc:
            old_proc = _tray_old_proc.pop(hwnd)
            _tray_callbacks.pop(hwnd, None)
            menu = _menu_handles.pop(hwnd, None)
            if menu:
                DestroyMenu(menu)
            try:
                SetWindowLongPtrW = user32.SetWindowLongPtrW
                SetWindowLongPtrW(hwnd, GWLP_WNDPROC,
                                  ctypes.cast(old_proc, ctypes.c_void_p).value)
            except AttributeError:
                SetWindowLongW(hwnd, GWL_WNDPROC,
                               ctypes.cast(old_proc, ctypes.c_void_p).value)
            return True
        return False

    # ---------- 右键上下文菜单 ----------
    _menu_id_counter = 1000

    def _get_next_menu_id():
        global _menu_id_counter
        _menu_id_counter += 1
        return _menu_id_counter

    def create_tray_menu():
        return CreatePopupMenu()

    def add_menu_item(menu, item_id, text, callback=None, is_separator=False):
        if is_separator:
            return AppendMenuW(menu, MF_SEPARATOR, 0, None)
        if callback:
            _menu_callbacks[item_id] = callback
        return AppendMenuW(menu, MF_STRING, item_id, text)

    def show_tray_menu(hwnd, menu):
        pt = POINT()
        if not GetCursorPos(ctypes.byref(pt)):
            return False
        SetForegroundWindow(hwnd)
        result = TrackPopupMenu(menu, TPM_LEFTALIGN | TPM_RIGHTBUTTON,
                                pt.x, pt.y, 0, hwnd, 0)
        user32.PostMessageW(hwnd, 0x0000, 0, 0)
        return bool(result)

    def setup_tray_context_menu(hwnd, items):
        """
        为托盘绑定右键菜单。
        items: 列表，元素为 (text, callback) 或 None（分隔符）
        返回菜单句柄，并自动保存至 _menu_handles 以供 show_tray_menu 使用。
        """
        menu = CreatePopupMenu()
        if not menu:
            return None
        for item in items:
            if item is None:
                AppendMenuW(menu, MF_SEPARATOR, 0, None)
            else:
                text, callback = item
                item_id = _get_next_menu_id()
                _menu_callbacks[item_id] = callback
                AppendMenuW(menu, MF_STRING, item_id, text)
        _menu_handles[hwnd] = menu
        return menu

    def destroy_tray_menu(menu):
        if menu:
            return bool(DestroyMenu(menu))
        return False

    # ---------- 开机自启动（基于注册表） ----------
    def set_auto_startup(enable: bool, name: str = None, app_path: str = None) -> bool:
        print(enable)
        """
        设置当前程序是否开机自启动（通过 HKEY_CURRENT_USER\...\Run）。
        :param enable:   True 启用，False 禁用
        :param name:     注册表项名称，默认为当前脚本/可执行文件的文件名（不含扩展名）
        :param app_path: 要启动的可执行文件完整路径。若为 None，默认使用 sys.executable。
                         对于脚本（.py）运行，建议传入完整的命令行，例如：
                         f'"{sys.executable}" "{sys.argv[0]}"'
        :return: 是否成功
        """
        if name is None:
            base = sys.argv[0].split('\\')[-1].split('/')[-1]
            if base.lower().endswith('.exe'):
                name = base[:-4]
            else:
                name = base.split('.')[0] or "DeskPet"

        if app_path is None:
            app_path = sys.executable

        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
            if enable:
                winreg.SetValueEx(key, name, 0, winreg.REG_SZ, app_path)
            else:
                try:
                    winreg.DeleteValue(key, name)
                except FileNotFoundError:
                    pass
            winreg.CloseKey(key)
            return True
        except Exception:
            return False

    def is_auto_startup_enabled(name: str = None) -> bool:
        """检查当前程序是否已设置为开机自启动"""
        if name is None:
            base = sys.argv[0].split('\\')[-1].split('/')[-1]
            if base.lower().endswith('.exe'):
                name = base[:-4]
            else:
                name = base.split('.')[0] or "DeskPet"

        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_READ)
            winreg.QueryValueEx(key, name)
            winreg.CloseKey(key)
            return True
        except FileNotFoundError:
            return False
        except Exception:
            return False

    # 退出时自动清理所有菜单
    @atexit.register
    def _cleanup_menus():
        for menu in _menu_handles.values():
            DestroyMenu(menu)
        _menu_handles.clear()

else:
    def get_window_handle_by_title(*args, **kwargs):
        raise NotImplementedError

    def set_transparent(*args, **kwargs):
        raise NotImplementedError

    def set_clickthrough(*args, **kwargs):
        raise NotImplementedError

    def set_topmost(*args, **kwargs):
        raise NotImplementedError

    def set_taskbar_visible(*args, **kwargs):
        raise NotImplementedError

    def get_taskbar_height(*args, **kwargs):
        raise NotImplementedError

    def set_window_focus(*args, **kwargs):
        raise NotImplementedError

    def load_icon_from_file(*args, **kwargs):
        raise NotImplementedError

    def set_window_icon(*args, **kwargs):
        raise NotImplementedError

    def create_single_instance_mutex(*args, **kwargs):
        raise NotImplementedError

    def add_tray_icon(*args, **kwargs):
        raise NotImplementedError

    def remove_tray_icon(*args, **kwargs):
        raise NotImplementedError

    def set_tray_callback(*args, **kwargs):
        raise NotImplementedError

    def remove_tray_callback(*args, **kwargs):
        raise NotImplementedError

    def create_tray_menu(*args, **kwargs):
        raise NotImplementedError

    def add_menu_item(*args, **kwargs):
        raise NotImplementedError

    def show_tray_menu(*args, **kwargs):
        raise NotImplementedError

    def setup_tray_context_menu(*args, **kwargs):
        raise NotImplementedError

    def destroy_tray_menu(*args, **kwargs):
        raise NotImplementedError

    def set_auto_startup(*args, **kwargs):
        raise NotImplementedError

    def is_auto_startup_enabled(*args, **kwargs):
        raise NotImplementedError

    def show_message_box(*args, **kwargs):
        raise NotImplementedError