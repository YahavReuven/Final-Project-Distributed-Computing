
import os

import consts
from errors import ParallelFunctionNotFoundError


def create_path_string(*directories, from_current_directory: bool = True) -> str:
    """
    Creates a string representing the path from the *directories.

    Args:
        *directories: the directories which make the full path.
        from_current_directory (bool) = True: whether or not to start
        the path from the current directory ("./").

    Returns:
        str: a string representing the desired path.
    """
    path = []
    if from_current_directory:
        path.append('.')

    for directory in directories:
        path.append(str(directory))

    return '\\'.join(path)
