from argparse import ArgumentParser

from ..files.location import find_preset_files
from ...__common__.display import print_application_header


def __add_arguments(parser: ArgumentParser) -> None:
    pass


def list_action(parser: ArgumentParser):
    """
    Display a list of profile configuration files installed on the system.

    Args:
        parser (ArgumentParser): an argument parser for further argument implementation if needed.
    """
    __add_arguments(parser)

    # Display
    print_application_header()
    print("List of installed profiles for this user:")
    for name, val in find_preset_files().items():
        print(f"\t-> [{val[0]}] {name:24s} | {val[1]}")
