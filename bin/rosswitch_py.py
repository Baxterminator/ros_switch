#!/usr/bin/env python3

from argparse import ArgumentParser
import sys
from enum import Enum

from ros_switch.commands import load, list_configs
from ros_switch.common.shell_msgs import error_msg


class Commands(Enum):
    LOAD = "load"
    LIST = "ls"
    GEN = "gen"
    NEW = "new"
    EXTEND = "extend"

    @staticmethod
    def is_value(txt: str) -> bool:
        """
        Return True if the value exist, false otherwise

        Args:
            txt (str): the command to find

        Returns:
            bool: True if the command exist, false otherwise
        """
        if txt == "-h" or txt == "--help":
            return True
        for cmd in Commands.__members__.values():
            if txt == cmd.value:
                return True
        return False


def setup_parser() -> ArgumentParser:
    """
    Setup the argument parser for the program

    Returns:
        ArgumentParser: the configured parser
    """
    parser = ArgumentParser(prog="rosswitch")
    sp = parser.add_subparsers(dest="command", required=True)

    # Load configuration arguments
    load_parser = sp.add_parser(Commands.LOAD.value)
    load_parser.add_argument("name")

    # List configurations arguments
    sp.add_parser(Commands.LIST.value)

    # Force regenerate a configuration arguments
    gen_parser = sp.add_parser(Commands.GEN.value)
    gen_parser.add_argument("name")

    # Create a new configuration arguments
    new_parser = sp.add_parser(Commands.NEW.value)
    new_parser.add_argument("name")

    # Extend an existing configuration arguments
    extend_parser = sp.add_parser(Commands.EXTEND.value)
    extend_parser.add_argument("parent")
    extend_parser.add_argument("child")

    return parser


if __name__ == "__main__":
    argc = len(sys.argv)
    parser = setup_parser()

    if len(sys.argv) == 2 and not Commands.is_value(sys.argv[1]):
        sys.argv.insert(1, Commands.LOAD.value)

    args = parser.parse_args()
    try:
        match Commands(args.command):
            case Commands.LOAD:
                print(load(args.name))
            case Commands.LIST:
                print(list_configs())
            case Commands.GEN:
                print("Regenerating configuration ...")
            case Commands.NEW:
                print("Creating new configuration ...")
            case Commands.EXTEND:
                print("Making new configuration from parent ...")
            case _:
                pass
    except RuntimeError as e:
        print(error_msg(f"The command {args.command} is not ok.\n{repr(e)}"))
