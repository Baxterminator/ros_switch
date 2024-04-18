from argparse import ArgumentParser
from enum import Enum
import sys

from ros_manage.profiles import list_action


class Commands(Enum):
    LIST = "ls"
    RM = "rm"
    LOAD = "load"
    EDIT = "edit"


def main():

    parser = declare_top_arguments()
    args = parser.parse_known_args()[0]

    match args.action:
        case Commands.LIST.value:
            list_action(parser)
        case Commands.RM.value:
            pass
        case Commands.LOAD.value:
            raise RuntimeError("Unimplemented method LOAD")
        case Commands.EDIT.value:
            raise RuntimeError("Unimplemented method EDIT")


def declare_top_arguments() -> ArgumentParser:
    """
    Declare Top-Level arguments for this executable

    Returns:
        ArgumentParser: _description_
    """
    possible_cmds = [m.value for _, m in Commands.__members__.items()]
    first_argv = sys.argv[1] if len(sys.argv) >= 2 else None

    if first_argv is not None:
        # Short loading arg
        if first_argv not in possible_cmds:
            sys.argv.insert(1, Commands.LOAD.value)

    parser = ArgumentParser(prog="ros_preset")

    # Add actions
    parser.add_argument("action", choices=possible_cmds)
    args = parser.parse_known_args()[0]

    # If not LIST cmd, get the preset we want to modify
    if args.action != Commands.LIST.value:
        parser.add_argument("preset")

    return parser


if __name__ == "__main__":
    main()
