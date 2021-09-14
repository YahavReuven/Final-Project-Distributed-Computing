
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


def validate_parallel_function(cls):
    """
    Checks if a parallel function is present in the given class.

    Raises:
        ParallelFunctionNotFound: if a parallel function is not
            defined in the class.
    """
    for attribute in dir(cls):
        if (callable(getattr(cls, attribute)) and
                attribute == consts.PARALLEL_FUNCTION_NAME):
            return
    raise ParallelFunctionNotFoundError
