from enum import Enum
import os
import platform
import ctypes
from typing import List, Tuple

# -----------------------------------------------------------------------------
# Applications
# -----------------------------------------------------------------------------
APP_NAME = "ros_switch"
AUTHOR = "Meltwin"
VERSION = "v1.0.0-alpha1"
YEAR = "2024"

ENV_RSWITCH_PRE = "RSWCH_"
ENV_CUSTOM_ADMIN_PATH = ENV_RSWITCH_PRE + "CUSTOM_ADMIN_PATHS"
ENV_CUSTOM_PATH = ENV_RSWITCH_PRE + "CUSTOM_PATHS"
PRESET_DIR = "profiles"
LOAD_DIR = "loader"
UNLOAD_DIR = "unloader"
PRESET_EXTENSION = ".rosprofile"


# -----------------------------------------------------------------------------
# Files
# -----------------------------------------------------------------------------
class OSType(Enum):
    WINDOWS = 0
    LINUX = 1
    MACOS = 2


match platform.system().lower():
    case "windows":
        OS_TYPE = OSType.WINDOWS
        IS_ADMIN = ctypes.windll.shell32.IsUserAnAdmin() != 0  # type: ignore
        # TODO: Set admin path for configuration
        ADMIN_CONF_DIR = ""
        if IS_ADMIN:
            CONF_DIR = ADMIN_CONF_DIR
        else:
            CONF_DIR = os.path.expandvars(os.path.join("%APPDATA%", APP_NAME))
        SCRIPT_EXT = ".bat"

    case "linux":
        OS_TYPE = OSType.LINUX
        IS_ADMIN = os.getuid() == 0
        ADMIN_CONF_DIR = os.path.join("/opt", "ros", APP_NAME)
        CONF_DIR = os.path.join(os.path.expanduser("~"), ".local", "share", APP_NAME)
        SCRIPT_EXT = ".sh"
    case "darwin":
        OS_TYPE = OSType.MACOS
        # TODO: Set admin path for configuration
        IS_ADMIN = os.getuid() == 0
        ADMIN_CONF_DIR = ""
        if IS_ADMIN:
            CONF_DIR = ADMIN_CONF_DIR
        else:
            CONF_DIR = os.path.join(
                os.path.expanduser("~"),
                "Library",
                "Preferences",
                APP_NAME,
            )
        SCRIPT_EXT = ".sh"


INSTALL_DIR = os.path.realpath(os.path.join(__file__, "..", "..", "..", ".."))


# Preset paths
def setup_paths() -> List[Tuple[str, bool]]:
    paths = [(INSTALL_DIR, True)]

    # ADMIN PATHS
    if ADMIN_CONF_DIR is not None and len(ADMIN_CONF_DIR) != 0:
        paths.append((ADMIN_CONF_DIR, True))
    for path in os.environ.get(ENV_CUSTOM_ADMIN_PATH, "").split(" "):
        if len(path) > 0:
            paths.append((path, True))

    # USER PATHS
    if CONF_DIR is not None and len(CONF_DIR) != 0:
        paths.append((CONF_DIR, False))
    for path in os.environ.get(ENV_CUSTOM_PATH, "").split(" "):
        if len(path) > 0:
            paths.append((path, False))

    return paths


PRESET_PATHS = setup_paths()
