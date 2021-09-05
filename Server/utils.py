import base64
import binascii

from errors import InvalidBase64Error


def validate_base64_and_decode(encoded: str, return_obj=True):
    try:
        obj = base64.b64decode(encoded)
    except binascii.Error:
        raise InvalidBase64Error
    if return_obj:
        return obj


# TODO: maybe replace with os.path.join
def create_path_string(*directories, from_current_directory: bool = True) -> str:
    """
    Creates a string representing the path from the *directories.

    Args:
        *directories: the directories which make the full path.
            The arguments given need to have a string representation.
        from_current_directory (bool) = True: whether or not to start
            the path from the current directory ('./').

    Returns:
        str: a string representing the desired path.

    """
    path = []
    if from_current_directory:
        path.append('.')

    for directory in directories:
        path.append(str(directory))

    return '\\'.join(path)

