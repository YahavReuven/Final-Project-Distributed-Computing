import base64
import binascii
import re
from datetime import timedelta

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

    return '/'.join(path)


# TODO: check function, external
def parse_timedelta(stamp):
    if 'day' in stamp:
        m = re.match(r'(?P<d>[-\d]+) day[s]*, (?P<h>\d+):'
                     r'(?P<m>\d+):(?P<s>\d[\.\d+]*)', stamp)
    else:
        m = re.match(r'(?P<h>\d+):(?P<m>\d+):'
                     r'(?P<s>\d[\.\d+]*)', stamp)
    if not m:
        raise ValueError

    time_dict = {key: float(val) for key, val in m.groupdict().items()}
    if 'd' in time_dict:
        return timedelta(days=time_dict['d'], hours=time_dict['h'],
                         minutes=time_dict['m'], seconds=time_dict['s'])
    else:
        return timedelta(hours=time_dict['h'],
                         minutes=time_dict['m'], seconds=time_dict['s'])



# def md5(password):
#     pass
#
# possible_passwords = []
#
# hashed_password = "..."
# for password in possible_passwords:
#     if md5(password) == hashed_password:
#         return password
#
#
# n = 5
#
#
# a = [0, 1] # fibonacci sequence
# for i in range(2, n+1):
#     a[i] = a[i - 1] + a[i - 2]
# return a[n]