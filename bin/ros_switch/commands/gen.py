from ..common.PresetData import PresetData
from .cmd_list import Commands
from ..utils.Arguments import ArgumentGroup
from ..common.ShellCom import Shell


@ArgumentGroup(Commands.GEN.value, ": (re-)generate the files for the given profile")
class GenArgs: ...


def generate_files(config_name: str) -> None:
    Shell.txt(f"Generating files for preset {config_name}")

    if config_name == "all":
        presets = PresetData.list_preset_files()
        for _, p in presets.items():
            p.generate_files()
    else:
        preset = PresetData.find_profile(config_name)
        if preset is None:
            raise RuntimeError(f"The preset {config_name} couldn't be found !")

        preset.generate_files()
