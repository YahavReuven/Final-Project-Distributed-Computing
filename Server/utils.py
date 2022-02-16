"""
Module used to provide utils.
"""
import base64
import binascii
import re
from datetime import timedelta

from errors import InvalidBase64Error


def validate_base64_and_decode(encoded: str, return_obj: bool = True):
    """
    Checks if the encoded base 64 is valid.

    Args:
        encoded (str): the base64 string.
        return_obj (bool) = True: whether to return the decoded string.

    Returns:
        bytes: the decoded base64.

    """
    try:
        obj = base64.b64decode(encoded)
    except binascii.Error:
        raise InvalidBase64Error
    if return_obj:
        return obj


def create_path_string(*directories: str, from_current_directory: bool = True) -> str:
    """
    Creates a string representing the path from the *directories.

    Args:
        *directories (str): the directories which make the full path.
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

    return '/'.join(path)


def parse_timedelta(str_repr: str):
    """
    Converts a timedelta string representation to timedelta.

    Args:
        str_repr (str): the string representation of the timedelta object.

    Returns:
        timedelta: the timedelta object.

    """
    if 'day' in str_repr:
        match_obj = re.match(r'(?P<d>[-\d]+) day[s]*, (?P<h>\d+):'
                             r'(?P<m>\d+):(?P<s>\d[\.\d+]*)', str_repr)
    else:
        match_obj = re.match(r'(?P<h>\d+):(?P<m>\d+):'
                             r'(?P<s>\d[\.\d+]*)', str_repr)
    if not match_obj:
        return ''

    time_dict = {key: float(val) for key, val in match_obj.groupdict().items()}
    if 'd' in time_dict:
        return timedelta(days=time_dict['d'], hours=time_dict['h'],
                         minutes=time_dict['m'], seconds=time_dict['s'])
    else:
        return timedelta(hours=time_dict['h'],
                         minutes=time_dict['m'], seconds=time_dict['s'])
