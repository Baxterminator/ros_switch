def __format_msg(txt: str) -> str:
    return txt.replace(" ", "%20").replace("\n", "%21").replace("\t", "%22")


def shell_msg(lvl: str, msg: str) -> str:
    return f"{lvl} {__format_msg(msg)}"


def error_msg(msg: str) -> str:
    return shell_msg("error", msg)


def txt_msg(msg: str) -> str:
    return shell_msg("txt", msg)


def load_msg(file: str) -> str:
    return shell_msg("load", file)
