
import os
import json

from utils import create_path_string
import consts
from errors import UserNotFoundError
from data_models import User
from handle_json import CustomDecoder

def validate_user_name(user_name: str):
    """
    Checks if the user with the name given exists.

    Args:
        user_name (str): the name of the user to check.

    Raises:
        UserNotFound: if the user was not found.

    """
    # TODO: only temporary
    file_path = create_path_string('C:\\Projects\\python\\final_project\\Client', consts.USERS_DIRECTORY, user_name + consts.JSON_EXTENSION,
                                   from_current_directory=False)
    if not os.path.isfile(file_path):
        raise UserNotFoundError


def get_device_id(user_name: str) -> str:
    data_file_path = create_path_string(consts.USERS_DIRECTORY,
                                        user_name + consts.JSON_EXTENSION)

    with open(data_file_path, 'r') as file:
        user = json.load(file, cls=CustomDecoder)

    return user.device_id


def get_user(user_name: str) -> User:
    # TODO: only temporary
    data_file_path = create_path_string('C:\\Projects\\python\\final_project\\Client', consts.USERS_DIRECTORY,
                                        user_name + consts.JSON_EXTENSION,
                                        from_current_directory=False)

    with open(data_file_path, 'r') as file:
        data = json.load(file)

    return User(**data)
