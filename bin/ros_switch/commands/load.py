import os

from .cmd_list import Commands
from ..common import PresetData
from ..common import Shell
from ..utils.Arguments import ArgumentGroup

from .unload import unload


@ArgumentGroup(Commands.LOAD.value)
class LoadArgs: ...


def load(config_name: str) -> None:
    # Unload any current preset if there's any
    unload()

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
