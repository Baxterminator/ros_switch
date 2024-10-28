import os

from .cmd_list import Commands
from ..common import PresetData
from ..common.ScriptGenerator import ScriptGenerator
from ..common import Shell
from ..utils.Arguments import ArgumentGroup


@ArgumentGroup(Commands.LOAD.value)
class LoadArgs: ...


def load(config_name: str) -> None:
    # Fetch the env var that contains the current loaded preset (if there's one)
    # If there's one, unload it before loading the new one
    current_preset = os.getenv(ScriptGenerator.PRESET_NAME_VAR)
    if current_preset is not None:
        preset = PresetData.find_profile(current_preset)
        if preset is None:
            raise RuntimeError("Current preset loaded cannot be found on known paths!")
        if preset.uninstall_script is None or not preset.is_generated():
            raise RuntimeError("Current preset does not have a known unload script!")
        Shell.load(preset.uninstall_script)

    # Load the wanted preset
    preset = PresetData.find_profile(config_name)
    if preset is None:
        raise RuntimeError(f"No preset is found with the name `{config_name}`")
    if preset.install_script is None:
        raise RuntimeError(
            f"Could not create the path to the install script of the preset `{config_name}` "
        )
    if not preset.is_generated():
        Shell.warning(
            f"The scripts for the preset `{config_name}` have not been generated!"
        )
        preset.generate_files()

    Shell.load(preset.install_script)
