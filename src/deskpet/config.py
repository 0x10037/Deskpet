import json
from deskpet.constants import SIZE_DEFAULT, FPS_DEFAULT, GRAVITY_DEFAULT, ACTION_SPEED_DEFAULT
from pathlib import Path
import sys


def _get_project_root():
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    else:
        return Path(__file__).parent.parent.parent


DEFAULT_CONFIG = {"size": SIZE_DEFAULT, "FPS": FPS_DEFAULT, "gravity": GRAVITY_DEFAULT,
                  "action_speed": ACTION_SPEED_DEFAULT, "first_open": True}
USER_DATA_DIR = _get_project_root()
DATA_PATH = USER_DATA_DIR / "data"
CONFIG_PATH = DATA_PATH / "settings.json"


class Config:
    def __init__(self):
        self.datas = load_config()

    def save(self, datas=None):
        if datas:
            self.datas = datas
        save_config(self.datas)

    def __getitem__(self, item):
        return self.datas[item]

    def __setitem__(self, key, value):
        self.datas[key] = value


def load_config():
    try:
        with open(CONFIG_PATH, "r") as f:
            config = json.load(f)
        if not config_check(config):
            config = DEFAULT_CONFIG
            set_default_config()
    except FileNotFoundError:
        config = DEFAULT_CONFIG
        set_default_config()
    return config


def save_config(config):
    print('save')
    set_default_config()
    try:
        with open(CONFIG_PATH, "w") as f:
            f.write(json.dumps(config, indent=4, sort_keys=True))
    except FileNotFoundError:
        pass


def set_default_config():
    DATA_PATH.mkdir(parents=True, exist_ok=True)
    with open(USER_DATA_DIR / "data" / "settings.json", "w") as f:
        f.write(json.dumps(DEFAULT_CONFIG, indent=4))


def config_check(config):
    try:
        return config["size"] and config["FPS"] and config["gravity"] and config["action_speed"]
    except:
        return False
