from ..common import Shell
from ..data.files.location import find_preset_files


ADMIN_SECTION = "Admin configuration:"
USER_SECTION = "User configurations:"
EOL = "\n"


def list_configs() -> None:
    # Get configs
    files = find_preset_files()

    # Export files as list
    msg = ADMIN_SECTION + EOL
    msg += "".ljust(len(ADMIN_SECTION), "-") + EOL
    if len(files["admin"].keys()) == 0:
        msg += "\tNo admin configurations found" + EOL
    else:
        for name, t in files["admin"].items():
            msg += f"\t- {name} -> {t[1]}" + EOL

    msg += EOL + USER_SECTION + EOL
    msg += "".ljust(len(USER_SECTION), "-") + EOL
    if len(files["user"].keys()) == 0:
        msg += "\tNo user configurations found" + EOL
    else:
        for name, t in files["user"].items():
            msg += f"\t- {name} -> {t[1]}" + EOL

    Shell.txt(msg)
