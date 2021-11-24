
from datetime import datetime, timedelta
import re

import consts

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


def is_file_json(file_name: str) -> bool:
    """
    If a file has the json extension.
    Args:
        file_name:

    Returns:

    """
    return file_name.endswith('.json')


# TODO: check function, external
def parse_timedelta(stamp):
    if 'day' in stamp:
        m = re.match(r'(?P<d>[-\d]+) day[s]*, (?P<h>\d+):'
                     r'(?P<m>\d+):(?P<s>\d[\.\d+]*)', stamp)
    else:
        m = re.match(r'(?P<h>\d+):(?P<m>\d+):'
                     r'(?P<s>\d[\.\d+]*)', stamp)
    if not m:
        return ''

    time_dict = {key: float(val) for key, val in m.groupdict().items()}
    if 'd' in time_dict:
        return timedelta(days=time_dict['d'], hours=time_dict['h'],
                         minutes=time_dict['m'], seconds=time_dict['s'])
    else:
        return timedelta(hours=time_dict['h'],
                         minutes=time_dict['m'], seconds=time_dict['s'])
