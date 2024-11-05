from enum import Enum
from colorama import Fore, Back, Style


class ColorValue(Enum):
    # Classic
    BLACK = "black"
    RED = "red"
    GREEN = "green"
    YELLOW = "yellow"
    BLUE = "blue"
    PURPLE = "purple"
    CYAN = "cyan"
    WHITE = "white"

    # Light
    LIGHT_BLACK = "lblack"
    LIGHT_RED = "lred"
    LIGHT_GREEN = "lgreen"
    LIGHT_YELLOW = "lyellow"
    LIGHT_BLUE = "lblue"
    LIGHT_PURPLE = "lpurple"
    LIGHT_CYAN = "lcyan"
    LIGHT_WHITE = "lwhite"

    # Bold
    BOLD_BLACK = "bblack"
    BOLD_RED = "bred"
    BOLD_GREEN = "bgreen"
    BOLD_YELLOW = "byellow"
    BOLD_BLUE = "bblue"
    BOLD_PURPLE = "bpurple"
    BOLD_CYAN = "bcyan"
    BOLD_WHITE = "bwhite"

    # Bold Light
    BOLD_LIGHT_BLACK = "blblack"
    BOLD_LIGHT_RED = "blred"
    BOLD_LIGHT_GREEN = "blgreen"
    BOLD_LIGHT_YELLOW = "blyellow"
    BOLD_LIGHT_BLUE = "blblue"
    BOLD_LIGHT_PURPLE = "blpurple"
    BOLD_LIGHT_CYAN = "blcyan"
    BOLD_LIGHT_WHITE = "blwhite"


class Color:

    BASH_SUFFIX = Fore.RESET + Back.RESET + Style.RESET_ALL

    def __init__(self, color: str | ColorValue) -> None:
        self._color: ColorValue
        if type(color) is str:
            self._color = ColorValue(color)
        else:
            self._color = color  # type: ignore
        self.term_color = self.__mk_zsh_color()

    def __mk_zsh_color(self) -> str:
        match self._color:
            # Classic
            case ColorValue.BLACK:
                return Back.BLACK + Fore.WHITE
            case ColorValue.RED:
                return Back.RED + Fore.WHITE
            case ColorValue.GREEN:
                return Back.GREEN + Fore.BLACK
            case ColorValue.YELLOW:
                return Back.YELLOW + Fore.BLACK
            case ColorValue.BLUE:
                return Back.BLUE + Fore.WHITE
            case ColorValue.PURPLE:
                return Back.MAGENTA + Fore.WHITE
            case ColorValue.CYAN:
                return Back.CYAN + Fore.WHITE
            case ColorValue.WHITE:
                return Back.WHITE + Fore.BLACK
            # Light
            case ColorValue.LIGHT_BLACK:
                return Back.LIGHTBLACK_EX + Fore.WHITE
            case ColorValue.LIGHT_RED:
                return Back.LIGHTRED_EX + Fore.WHITE
            case ColorValue.LIGHT_GREEN:
                return Back.LIGHTGREEN_EX + Fore.BLACK
            case ColorValue.LIGHT_YELLOW:
                return Back.LIGHTYELLOW_EX + Fore.BLACK
            case ColorValue.LIGHT_BLUE:
                return Back.LIGHTBLUE_EX + Fore.WHITE
            case ColorValue.LIGHT_PURPLE:
                return Back.LIGHTMAGENTA_EX + Fore.WHITE
            case ColorValue.LIGHT_CYAN:
                return Back.LIGHTCYAN_EX + Fore.BLACK
            case ColorValue.LIGHT_WHITE:
                return Back.LIGHTWHITE_EX + Fore.BLACK
            # Bold
            case ColorValue.BOLD_BLACK:
                return Style.BRIGHT + Back.BLACK + Fore.WHITE
            case ColorValue.BOLD_RED:
                return Style.BRIGHT + Back.RED + Fore.WHITE
            case ColorValue.BOLD_GREEN:
                return Style.BRIGHT + Back.GREEN + Fore.BLACK
            case ColorValue.BOLD_YELLOW:
                return Style.BRIGHT + Back.YELLOW + Fore.BLACK
            case ColorValue.BOLD_BLUE:
                return Style.BRIGHT + Back.BLUE + Fore.WHITE
            case ColorValue.BOLD_PURPLE:
                return Style.BRIGHT + Back.MAGENTA + Fore.WHITE
            case ColorValue.BOLD_CYAN:
                return Style.BRIGHT + Back.CYAN + Fore.WHITE
            case ColorValue.BOLD_WHITE:
                return Style.BRIGHT + Back.WHITE + Fore.BLACK
            # Bold light
            case ColorValue.BOLD_LIGHT_BLACK:
                return Style.BRIGHT + Back.LIGHTBLACK_EX + Fore.WHITE
            case ColorValue.BOLD_LIGHT_RED:
                return Style.BRIGHT + Back.LIGHTRED_EX + Fore.WHITE
            case ColorValue.BOLD_LIGHT_GREEN:
                return Style.BRIGHT + Back.LIGHTGREEN_EX + Fore.BLACK
            case ColorValue.BOLD_LIGHT_YELLOW:
                return Style.BRIGHT + Back.LIGHTYELLOW_EX + Fore.BLACK
            case ColorValue.BOLD_LIGHT_BLUE:
                return Style.BRIGHT + Back.LIGHTBLUE_EX + Fore.WHITE
            case ColorValue.BOLD_LIGHT_PURPLE:
                return Style.BRIGHT + Back.LIGHTMAGENTA_EX + Fore.WHITE
            case ColorValue.BOLD_LIGHT_CYAN:
                return Style.BRIGHT + Back.LIGHTCYAN_EX + Fore.BLACK
            case ColorValue.BOLD_LIGHT_WHITE:
                return Style.BRIGHT + Back.WHITE + Fore.BLACK
