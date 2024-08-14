from enum import Enum
import os
import platform
import ctypes

# -----------------------------------------------------------------------------
# Applications
# -----------------------------------------------------------------------------
APP_NAME = "ros_switch"
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
        IS_ADMIN = ctypes.windll.shell32.IsUserAnAdmin() != 0  # type: ignore
        # TODO: Set admin path for configuration
        ADMIN_CONF_DIR = ""
        if IS_ADMIN:
            CONF_DIR = ADMIN_CONF_DIR
        else:
            CONF_DIR = os.path.expandvars(os.path.join("%APPDATA%", APP_NAME))

    case "Linux":
        OS_TYPE = OSType.LINUX
        IS_ADMIN = os.getuid() == 0
        ADMIN_CONF_DIR = os.path.join("/opt", "ros", APP_NAME)
        if IS_ADMIN:
            CONF_DIR = ADMIN_CONF_DIR
        else:
            CONF_DIR = os.path.join(
                os.path.expanduser("~"), ".local", "share", APP_NAME
            )
    case "Darwin":
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


INSTALL_DIR = os.path.realpath(os.path.join(__file__, "..", "..", "..", ".."))
