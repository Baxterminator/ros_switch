from os import path


def read_file(f: str) -> str | None:
    """
    Open the given file and read its content. If the file doesn't exist throw an

    :param f:
    :return:
    """
    if not path.exists(f):
        raise RuntimeError(f"Path {f} does not exist!")

    data = None
    with open(f, "r") as data_file:
        data = data_file.read()
    return data
