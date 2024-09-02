class Shell:
    buffer = ""

    @staticmethod
    def __format_msg(txt: str) -> str:
        return f"{txt}".replace(" ", "%20").replace("\n", "%21").replace("\t", "%22")

    @staticmethod
    def msg(lvl: str, msg: str) -> None:
        Shell.buffer += f" {lvl} {Shell.__format_msg(msg)}"

    @staticmethod
    def error(msg: str) -> None:
        Shell.msg("error", msg)

    @staticmethod
    def txt(msg: str) -> None:
        Shell.msg("txt", msg)

    @staticmethod
    def load(file: str) -> None:
        Shell.msg("load", file)

    @staticmethod
    def str() -> str:
        return Shell.buffer
