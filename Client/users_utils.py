"""
Module contains helper functions regarding the users.
"""
import os

from utils import create_path_string, is_file_json
import consts


def get_users_names() -> list:
    users_path = create_path_string(consts.USERS_DIRECTORY)

    dirs = os.listdir(users_path)

    names = []

    for file_name in dirs:
        if is_file_json(file_name):
            name_parts = file_name.split('.')
            names.append('.'.join(name_parts[:-1]))

    return names
