"""
Module used to initialize the application.
"""

import os

from utils import create_path_string
import consts
from handle_users_data import UsersDataHandler


def init_user():
    users_path = create_path_string(consts.USERS_DIRECTORY)
    os.makedirs(users_path, exist_ok=True)

    user_name = input('please enter the user name: ')
    return UsersDataHandler(user_name)


def init_tasks():
    tasks_path = create_path_string(consts.TASKS_DIRECTORY)
    os.makedirs(tasks_path, exist_ok=True)


