
import os
import json

from utils import create_path_string
import consts
from errors import UserNotFound


def validate_user_name(user_name: str):
    """
    Checks if the user with the name given exists.

    Args:
        user_name (str): the name of the user to check.

    Raises:
        UserNotFound: if the user was not found.

    """
    file_path = create_path_string(consts.USERS_DIRECTORY, user_name + consts.JSON_EXTENSION)
    if not os.path.isfile(file_path):
        raise UserNotFound


def get_device_id(user_name: str) -> str:
    data_file_path = create_path_string(consts.USERS_DIRECTORY, user_name,
                                        consts.JSON_EXTENSION)

    with open(data_file_path, 'r') as file:
        data = json.load(file)

    return data[consts.DATA_DEVICE_ID_KEY]
