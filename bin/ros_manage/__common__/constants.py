from enum import Enum
import os
import platform
import ctypes

# -----------------------------------------------------------------------------
# Applications
# -----------------------------------------------------------------------------
APP_NAME = "ros_manage"
AUTHOR = "Meltwin"
VERSION = "v1.0"
YEAR = "2024"


# -----------------------------------------------------------------------------
# Files
# -----------------------------------------------------------------------------
class OSType(Enum):
    WINDOWS = 0
    LINUX = 1
    MACOS = 2


match platform.system():
    case "Windows":
        OS_TYPE = OSType.WINDOWS
        CONF_DIR = os.path.expandvars(os.path.join("%APPDATA%", APP_NAME))
        IS_ADMIN = ctypes.windll.shell32.IsUserAnAdmin() != 0 # type: ignore
    case "Linux":
        OS_TYPE = OSType.LINUX
        CONF_DIR = os.path.join(os.path.expanduser("~"), ".local", "share", APP_NAME)
        IS_ADMIN = os.getuid() == 0
    case "Darwin":
        OS_TYPE = OSType.MACOS
        CONF_DIR = os.path.join(
            os.path.expanduser("~"),
            "Library",
            "Preferences",
            APP_NAME,
        )
        IS_ADMIN = os.getuid() == 0

INSTALL_DIR = os.path.realpath(os.path.join(__file__, "..", "..", "..", ".."))
