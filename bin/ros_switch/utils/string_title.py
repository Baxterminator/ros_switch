from enum import Enum
from re import A
from typing import List
from colorama import Fore


class Justify(Enum):
    LEFT = "#ljust"
    CENTER = "#center"
    RIGHT = "#rjust"

    @staticmethod
    def is_just(val: "str | Justify"):
        for m, v in Justify.__members__.items():
            if val == v:
                return True
        return False


class StrSections:
    H_LINE_CHAR = "-"
    V_LINE_CHAR = "|"
    CORNER_CHAR = "+"
    FILL_CHAR = " "
    FILL_CHAR_COLOR = None
    HEADER_WIDTH = 80

    @staticmethod
    def make_underlined_section(
        txt: str,
        line_char=H_LINE_CHAR,
        delta_line=2,
        line_color: str | None = None,
        line_prefix="",
    ) -> str:
        line_pre = "" if line_color is None else line_color
        line_post = "" if line_color is None else Fore.RESET
        return "{4}{0}:\n{4}{2}{1}{3}".format(
            txt,
            "".ljust(len(txt) + delta_line, line_char),
            line_pre,
            line_post,
            line_prefix,
        )

    @staticmethod
    def make_enclosed_section(
        txt: str,
        width=HEADER_WIDTH,
        linechar=H_LINE_CHAR,
        line_color: str | None = None,
        line_prefix="",
    ) -> str:
        line_pre = "" if line_color is None else line_color
        line_post = "" if line_color is None else Fore.RESET

        line = "".ljust(width, linechar)
        out = "{4}{2}{0}{3}\n{4}{1}\n{4}{2}{0}{3}\n".format(
            line,
            txt,
            line_pre,
            line_post,
            line_prefix,
        )
        return out

    @staticmethod
    def make_header(
        txt: str | List[str | Justify],
        hline_char=H_LINE_CHAR,
        vline_char=V_LINE_CHAR,
        corner_char=CORNER_CHAR,
        fill_char=FILL_CHAR,
        fill_char_color: str | None = None,
        width=HEADER_WIDTH,
        line_prefix="",
        base_justify=Justify.CENTER,
    ) -> str:
        line = "{2}{0}{1}{0}\n".format(
            corner_char,
            "".ljust(width - 2, hline_char),
            line_prefix,
        )
        out = str(line)

        fill_pre = fill_char_color if fill_char_color is not None else ""
        fill_post = Fore.RESET if fill_char_color is not None else ""

        def make_line(line: str, just: Justify) -> str:
            l = f"{fill_post}{line}{fill_pre}"
            args = [width + 4 * len(fill_pre) - 4, fill_char]

            lengthen = l
            match just:
                case Justify.LEFT:
                    lengthen = lengthen.ljust(*args)
                case Justify.CENTER:
                    lengthen = lengthen.center(*args)
                case Justify.RIGHT:
                    lengthen = lengthen.rjust(*args)

            return "{0}{1}{2}{5}{3}{5}{4}{1}\n".format(
                line_prefix,
                vline_char,
                fill_pre,
                lengthen,
                fill_post,
                fill_char,
            )

        # Put text
        justify = base_justify
        if type(txt) is list:
            for l in txt:
                if Justify.is_just(l):
                    justify = Justify(l)
                else:
                    out += make_line(l, justify)  # type: ignore
        else:
            out += make_line(txt)  # type: ignore

        out += line
        return out
