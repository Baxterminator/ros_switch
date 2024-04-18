from .box_gen import gen_box
from math import floor


def gen_title(
    stdscr,
    msg: str,
    width: int,
    height: int = 3,
    row0: int = 0,
    col0: int = 0,
) -> None:
    """
    Gen a title box

    Args:
        msg (str): _description_
    """
    # Gen box
    for row, col, ch in gen_box(width, height):
        stdscr.addstr(row0 + row, col0 + col, ch)

    stdscr.addstr(row0 + floor(height // 2), col0 + 1, msg.center(width - 2, " "))
