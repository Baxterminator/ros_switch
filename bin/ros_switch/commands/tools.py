from enum import Enum
from typing import List

from ..common.ShellCom import Shell


class ToolsChoices(Enum):
    COLORS = "colors"

    @staticmethod
    def get_vals() -> List[str]:
        return [v.value for _, v in ToolsChoices.__members__.items()]


def tools_section(tool_action: str):
    try:
        act = ToolsChoices(tool_action)

        match act:
            case ToolsChoices.COLORS:
                _display_colors()

    except:
        Shell.error(f"Unknown tool action: `{tool_action}`")


def _display_colors():
    LETTERS = r"abcdefghijklmnopqrstuvwxyz"
    NUMBERS = r"0123456789"
    OTHERS = r"-_"
    from ..utils.data.Color import Color, ColorValue

    txt = "{}{}{}{}".format(LETTERS, LETTERS.upper(), NUMBERS, OTHERS)
    txt = "{0}{1}{0}".format("{}", txt)

    Shell.start_section("Available colors for presets")

    for _, v in ColorValue.__members__.items():
        c = Color(v)
        Shell.txt(
            f"{f'{v.value} '.ljust(20, '.')} -> {txt.format(c.term_color, c.BASH_SUFFIX)}"
        )
