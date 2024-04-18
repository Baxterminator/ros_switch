import os
from typing import Dict, List, Tuple

from ...__common__.constants import CONF_DIR, INSTALL_DIR, IS_ADMIN

# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------

PRESET_DIR = "profiles"
PRESET_EXT = ".rosprof"

# -----------------------------------------------------------------------------
# Names
# -----------------------------------------------------------------------------


def file2preset_name(file_name: str) -> str:
    return file_name.split(".")[0].replace("_", " ").title()


def preset_name2file(preset_name: str) -> str:
    return preset_name.lower().replace(" ", "_") + PRESET_EXT


# -----------------------------------------------------------------------------
# User configs
# -----------------------------------------------------------------------------


def __find_profiles_in_dir(
    dirpath: str,
    tag: str,
    existing_names: List[str] = [],
) -> Dict[str, Tuple[str, str]]:
    """
    Walk the dir to find the ros profile configuration files.

    Args:
        dirpath (str): the path to look into for conf files

    Returns:
        Dict[str, Tuple[str, str]]: a map (k,v) of {preset_name: (tag, preset_path)}
    """
    # Test for directory to exist
    if not os.path.exists(dirpath):
        return {}

    out = {}
    for dpath, _, filenames in os.walk(os.path.join(dirpath, PRESET_DIR)):
        for f in filenames:
            # Check if profile file
            if not f.endswith(PRESET_EXT):
                continue

            # Compute simple name
            preset_name = file2preset_name(f)

            # Test if name already used
            if preset_name in out.keys() or preset_name in existing_names:
                i = 1
                new_preset = f"{preset_name}_{i}"
                while new_preset in out.keys() or new_preset in existing_names:
                    i += 1
                    new_preset = f"{preset_name}_{i}"
                preset_name = new_preset

            out[preset_name] = (tag, os.path.join(dpath, f))
    return out


def find_admin_configs() -> Dict[str, Tuple[str, str]]:
    """
    Find the preset made by the admin

    Returns:
        Dict[str, Tuple[str, str]]: a map (k,v) of {preset_name: (tag, preset_path)}
    """
    return __find_profiles_in_dir(INSTALL_DIR, "ADMIN")


def find_user_configs(existing_name: List[str]) -> Dict[str, Tuple[str, str]]:
    """
    Find the preset made by the user

    Returns:
        Dict[str, Tuple[str, str]]: a map (k,v) of {preset_name: (tag, preset_path)}
    """
    return __find_profiles_in_dir(CONF_DIR, "USER ", existing_name)


def find_preset_files() -> Dict[str, Tuple[str, str]]:
    """
    Find all presets found on the system

    Returns:
        Dict[str, Tuple[str, str]]: a map (k,v) of {preset_name: (tag, preset_path)}
    """
    admin = find_admin_configs()
    return {**admin, **find_user_configs(admin.keys())}  # type: ignore
