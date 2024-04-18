from typing import Iterator, Tuple


class Char:
    # Specials
    H = "═"
    V = "║"
    M = "╬"

    # Corners
    C_TR = "╗"
    C_BR = "╝"
    C_TL = "╔"
    C_BL = "╚"

    # T shapes
    T_RLB = "╦"
    T_TBL = "╣"
    T_TBR = "╠"
    T_RLT = "╩"


def gen_box(
    width: int,
    height: int,
    link_left: bool = False,
    link_top: bool = False,
    down_box_exist: bool = False,
    right_box_exist: bool = False,
) -> Iterator[Tuple[int, int, str]]:
    """
    Generate a bounding box given width and height

    Args:
        width (int): the width of the the box
        height (int): the height of the box
        link_left (bool): whether a box exist on the left, if true won't generate the first column
        link_top (bool): whether a box exist at the top, if true won't generate the first row
        down_box_exist (bool): whether a box exist below, it will adapt the corners
        right_box_exist (bool): whether a box exist at the right, it will adapt the corners

    Yields:
        Iterator[int, int, chr]: an iterator (x, y, char) to display
    """
    # Top-Right corner
    TR_C = Char.T_RLB if right_box_exist else Char.C_TR
    BL_C = Char.T_TBR if down_box_exist else Char.C_BL
    if down_box_exist:
        BR_C = Char.M if right_box_exist else Char.T_TBL
    else:
        BR_C = Char.T_RLT if right_box_exist else Char.C_BR

    # Top line
    if not link_top:
        yield (0, 0, Char.C_TL)  # Corner
        for col in range(1, width - 1):
            yield (0, col, Char.H)
        yield (0, width - 1, TR_C)  # Corner

    # Intermediate lines
    for row in range(1, height - 1):
        # First column
        if not link_left:
            yield (row, 0, Char.V)

        # Last column
        yield (row, width - 1, Char.V)

    # Last line
    if not link_left:
        yield (height - 1, 0, BL_C)
    for col in range(1, width - 1):
        yield (height - 1, col, Char.H)
    yield (height - 1, width - 1, BR_C)
