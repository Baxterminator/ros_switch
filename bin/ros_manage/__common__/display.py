from typing import List

from .constants import APP_NAME, AUTHOR, YEAR, VERSION

DISP_WIDTH = 80


def print_header(text: List[str], width: int = DISP_WIDTH) -> None:
    print("".center(width, "="))
    for line in text:
        print(line.center(width, " "))
    print("".center(width, "="))


def print_application_header() -> None:
    print_header(
        [
            f'{APP_NAME.replace("_", " ").upper()} {VERSION}',
            f"Copyright (c) {AUTHOR}, {YEAR}",
        ]
    )
