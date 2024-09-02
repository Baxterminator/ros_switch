#!/usr/bin/env python3

# =============================================================================
#                               ROS SWITCH
# ROS Switch is a project that let you switch between several ROS environments
# based on YAML Configurations files. It aims to be highly customizable while
# remaining simple enough while using it
# =============================================================================

from argparse import ArgumentParser
from math import pi
import sys
from enum import Enum

from ros_switch.commands import load, list_configs
from ros_switch.common import Shell


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
    parser.add_argument("-d", "--debug", dest="debug", action="store_true")
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

    # If no command is provided, consider it as a configuration file
    # This provide
    if len(sys.argv) == 2 and not Commands.is_value(sys.argv[1]):
        sys.argv.insert(1, Commands.LOAD.value)

    Shell.txt("Test 1")
    Shell.txt("Test 2")

    args = parser.parse_args()
    try:
        match Commands(args.command):
            case Commands.LOAD:
                load(args.name)
            case Commands.LIST:
                list_configs()
            case Commands.GEN:
                Shell.txt("Regenerating configuration ...")
            case Commands.NEW:
                Shell.txt("Creating new configuration ...")
            case Commands.EXTEND:
                Shell.txt("Making new configuration from parent ...")
            case _:
                pass
    except RuntimeError as e:
        Shell.error(f"The command {args.command} is not ok.\n{repr(e)}")
    finally:
        print(Shell.str())
