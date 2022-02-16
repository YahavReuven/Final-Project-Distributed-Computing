"""
Module used to handle
"""
import os
import json
from pathlib import Path

import consts
from utils import create_path_string
from errors import UserNotFoundError
from data_models import User
from handle_json import CustomDecoder


def get_user_name_path(user_name: str) -> str:
    """
    Creates the path of a user's data file.

    Args:
        user_name (str): the name of the desired user.

    Returns:
        str: the path of the user's data file.

    """
    return create_path_string(str(Path.home()), consts.APP_NAME, consts.USERS_DIRECTORY,
                              user_name + consts.JSON_EXTENSION,
                              from_current_directory=False)


def validate_user_name(user_name: str):
    """
    Checks if the user with the given name exists.

    Args:
        user_name (str): the name of the user to check.

    Raises:
        UserNotFound: if the user was not found.

    """
    file_path = get_user_name_path(user_name)
    if not os.path.isfile(file_path):
        raise UserNotFoundError


def get_user(user_name: str) -> User:
    """
    Gets a user based on its name.

    Args:
        user_name (str): the name of the user.

    Returns:
        User: the user.

    """
    data_file_path = get_user_name_path(user_name)
    with open(data_file_path, 'r') as file:
        user = json.load(file, cls=CustomDecoder)

    return user
