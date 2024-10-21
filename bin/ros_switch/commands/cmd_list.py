from enum import Enum


class Commands(Enum):
    LOAD = "load"
    LIST = "ls"
    GEN = "gen"
    NEW = "new"
    EXTEND = "extend"

    @staticmethod
    def is_value(txt: str) -> bool:
        """
        Return True if the value exist, false otherwise

        Args:
            txt (str): the command to find

        Returns:
            bool: True if the command exist, false otherwise
        """
        if txt == "-h" or txt == "--help":
            return True
        for cmd in Commands.__members__.values():
            if txt == cmd.value:
                return True
        return False
