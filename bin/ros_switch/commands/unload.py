import os

from ..common import PresetData
from ..common.generator.ScriptGenerator import Vars
from ..common import Shell


def unload():
    # Fetch the env var that contains the current loaded preset (if there's one)
    # If there's one, unload it before loading the new one
    current_preset = os.getenv(Vars.PRESET_NAME)
    if current_preset is not None:
        preset = PresetData.find_profile(current_preset)
        if preset is None:
            raise RuntimeError("Current preset loaded cannot be found on known paths!")
        if preset.uninstall_script is None or not preset.is_generated():
            raise RuntimeError("Current preset does not have a known unload script!")
        Shell.load(preset.uninstall_script)
