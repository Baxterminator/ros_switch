from colorama import Fore
from .constants import APP_NAME, AUTHOR, VERSION, YEAR
from ..utils.string_title import StrSections


class Shell:
    """
    Class that allow communication of messages and orders to the shell.
    Works as static methods.
    Implemented methods:
        - txt: basic logging messages
        - error: error display
        - load: ask to source a file to load its content in the shell
    """

    buffer = ""
    _IN_DEBUG = False
    TAB_SIZE = 4

    @staticmethod
    def enable_debug_msgs(state: bool = True) -> None:
        Shell._IN_DEBUG = state

    # =========================================================================
    # Low level transfert function
    # =========================================================================

    @staticmethod
    def __format_msg(txt: str) -> str:
        return (
            txt.replace("".ljust(Shell.TAB_SIZE, " "), "\t")
            .replace(" ", "%20")
            .replace("\n", "%21")
            .replace("\t", "%22")
        )

    @staticmethod
    def msg(lvl: str, msg: str) -> None:
        Shell.buffer += f" {lvl} {Shell.__format_msg(msg)}"

    @staticmethod
    def to_str() -> str:
        return Shell.buffer

    # =========================================================================
    # Shell communication functions
    # =========================================================================

    @staticmethod
    def txt(msg: str) -> None:
        Shell.msg("txt", msg)

    @staticmethod
    def debug(msg: str) -> None:
        if Shell._IN_DEBUG:
            Shell.txt(f"{Fore.GREEN}[DEBUG] {msg}{Fore.RESET}")

    @staticmethod
    def error(msg: str) -> None:
        Shell.txt(f"{Fore.RED}[ERROR] {msg}{Fore.RESET}")

    @staticmethod
    def warning(msg: str) -> None:
        Shell.txt(f"{Fore.YELLOW}[WARN] {msg}{Fore.RESET}")

    @staticmethod
    def load(file: str) -> None:
        Shell.msg("load", file)

    # =========================================================================
    # High-level messages
    # =========================================================================

    HEADER_WIDTH = 80
    SHELL_FILLING = r"~"
    LINE_CHAR = r"-"
    HIDDEN_COLOR = Fore.BLACK

    @staticmethod
    def start_section(section_title: str) -> None:
        Shell.txt(
            StrSections.make_underlined_section(
                f"¤ {section_title}", line_color=Fore.CYAN
            )
        )

    @staticmethod
    def print_header() -> None:
        Shell.txt(
            StrSections.make_header(
                [
                    f"{Fore.YELLOW}{APP_NAME.upper()} - {VERSION}{Shell.HIDDEN_COLOR}",
                    f"{Fore.CYAN}(c) {AUTHOR} - {YEAR}{Shell.HIDDEN_COLOR}",
                ],
                fill_char=Shell.SHELL_FILLING,
                fill_char_color=Shell.HIDDEN_COLOR,
                width=Shell.HEADER_WIDTH,
            )
        )
