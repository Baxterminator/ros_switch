from colorama import Fore

from ..common import Shell
from ..common import PresetData
from .cmd_list import Commands
from ..utils.Arguments import ArgumentGroup


ADMIN_SECTION = "Admin configuration"
USER_SECTION = "User configurations"


@ArgumentGroup(Commands.LIST.value, ": list all known custom profiles")
class ListArgs: ...


def list_configs() -> None:
    # Get configs
    files = PresetData.list_preset_files()

    # Export files as list
    Shell.txt(f"Found {len(files)} configurations")
    Shell.start_section(ADMIN_SECTION)
    has_one = False
    for preset_name, data in files.items():
        if data.is_admin:
            has_one = True
            pre = (
                f"[{Fore.GREEN}{'OK'.center(7)}{Fore.RESET}]"
                if data.is_generated()
                else f"[{Fore.RED}{'NOT GEN'.center(7)}{Fore.RESET}]"
            )
            Shell.txt(f"\t- {pre} {preset_name} -> {data.preset_file}")
    if not has_one:
        Shell.txt("\tNo admin configurations found")

    Shell.start_section("\n" + USER_SECTION)
    has_one = False
    for preset_name, data in files.items():
        if not data.is_admin:
            has_one = True
            pre = (
                f"[{Fore.GREEN}{'OK'.center(7)}{Fore.RESET}]"
                if data.is_generated()
                else f"[{Fore.RED}{'NOT GEN'.center(7)}{Fore.RESET}]"
            )
            Shell.txt(f"\t- {pre} {preset_name} -> {data.preset_file}")
    if not has_one:
        Shell.txt("\tNo user configurations found")
