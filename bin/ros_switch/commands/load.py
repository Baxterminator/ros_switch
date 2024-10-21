from ..common import Shell
from .cmd_list import Commands
from ..utils.Arguments import ArgumentGroup, Argument


@ArgumentGroup(Commands.LOAD.value)
class LoadArgs: ...


def load(config_name: str) -> None:

    Shell.load("")
