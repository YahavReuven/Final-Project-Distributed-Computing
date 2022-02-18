"""
Module used to provide utils.
"""
import re
import os
import stat
from datetime import timedelta


def create_path_string(*directories: str, from_current_directory: bool = True) -> str:
    """
    Creates a string representing the path from the *directories.

    Args:
        *directories (str): the directories which make the full path.
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
    return '/'.join(path)


def is_file_json(file_name: str) -> bool:
    """
    If a file has the json extension.

    Args:
        file_name (str): the name of the file.

    Returns:
        bool: whether the file is a json file.

    """
    return file_name.endswith('.json')


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


def rmtree_onerror_remove_readonly(func, path, _):
    """
    Clear the readonly bit and reattempt the removal.

    Note:
         is called only by rmtree.

    """
    os.chmod(path, stat.S_IWRITE)
    func(path)
