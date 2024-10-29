#!/usr/bin/env python3

# =============================================================================
#                               ROS SWITCH
# ROS Switch is a project that let you switch between several ROS environments
# based on YAML Configurations files. It aims to be highly customizable while
# remaining simple enough while using it
# =============================================================================

from argparse import ArgumentParser
import sys

from ros_switch.commands import (
    Commands,
    load,
    list_configs,
    ListArgs,
    generate_files,
    GenArgs,
    ToolsChoices,
    tools_section,
)
from ros_switch.common import Shell

from ros_switch.commands.list import ListArgs


def setup_parser() -> ArgumentParser:
    """
    Setup the argument parser for the program

    Returns:
        ArgumentParser: the configured parser
    """
    parser = ArgumentParser(prog="rosswitch")
    parser.add_argument(
        "-d",
        "--debug",
        dest="debug",
        action="store_true",
        help="display debug informations",
    )
    sp = parser.add_subparsers(dest="command", required=True)

    # Load configuration arguments

    load_parser = sp.add_parser(Commands.LOAD.value, help=": load a custom profile")
    load_parser.add_argument("name")

    # List configurations arguments
    ListArgs.setup_parser(sp)  # type: ignore

    # Force regenerate a configuration arguments
    # GenArgs.setup_parser(sp)  # type: ignore
    gen_parser = sp.add_parser(
        Commands.GEN.value,
        help=": (re-)generate the files for the given profile",
    )
    gen_parser.add_argument("name")

    # Create a new configuration arguments
    new_parser = sp.add_parser(
        Commands.NEW.value,
        help=": create a new profile with the given name",
    )
    new_parser.add_argument("name")

    # Extend an existing configuration arguments
    extend_parser = sp.add_parser(
        Commands.EXTEND.value,
        help=": create a new configuration based on the given one",
    )
    extend_parser.add_argument("parent")
    extend_parser.add_argument("new")

    debug_parser = sp.add_parser(
        Commands.TOOLS.value, help="Debug commands for testing"
    )
    debug_parser.add_argument("tool_action", type=str, choices=ToolsChoices.get_vals())

    return parser


if __name__ == "__main__":
    argc = len(sys.argv)
    parser = setup_parser()

    # If no command is provided, consider it as a configuration file
    # This provide
    if len(sys.argv) == 2 and not Commands.is_value(sys.argv[1]):
        sys.argv.insert(1, Commands.LOAD.value)

    # Test for help (special case for the shell escaping)
    if "-h" in sys.argv or "--help" in sys.argv:
        Shell.txt(parser.format_help())
        print(Shell.to_str())
        exit(0)

    # Process arguments
    args = parser.parse_args()

    # Enable debug messages ?
    Shell.enable_debug_msgs(args.debug)

    # Run command
    try:
        match Commands(args.command):
            case Commands.LOAD:
                load(args.name)
            case Commands.LIST:
                Shell.print_header()
                list_configs()
            case Commands.GEN:
                Shell.print_header()
                generate_files(args.name)
            case Commands.NEW:
                Shell.print_header()
                Shell.txt("Creating new configuration ...")
            case Commands.EXTEND:
                Shell.print_header()
                Shell.txt("Making new configuration from parent ...")
            case Commands.TOOLS:
                Shell.print_header()
                tools_section(args.tool_action)
            case _:
                pass
    except RuntimeError as e:
        Shell.error(e.__str__())
    finally:
        print(Shell.to_str())
