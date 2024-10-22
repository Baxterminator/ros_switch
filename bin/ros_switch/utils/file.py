import os


def read_file(f: str) -> str | None:
    """
    Open the given file and read its content. If the file doesn't exist throw an

    :param f:
    :return:
    """
    if not os.path.exists(f):
        raise RuntimeError(f"Path {f} does not exist!")

    data = None
    with open(f, "r") as data_file:
        data = data_file.read()
    return data


def mk_file_dir(f: str) -> str:
    """
    Make sur that the folder of the given file exist

    Args:
        f (str): the file path
    """
    d = os.path.expandvars(os.path.dirname(f))
    if not os.path.exists(d):
        os.mkdir(d)
    return d
