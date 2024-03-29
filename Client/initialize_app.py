"""
Module used to initialize the application.
"""
import os

import consts
from handle_users import switch_user
from utils import create_path_string


def init_user():
    """
    Initializes the users' directory and returns a user.
    """
    users_path = create_path_string(consts.USERS_DIRECTORY)
    os.makedirs(users_path, exist_ok=True, mode=0o777)
    return switch_user()


def init_task_storage():
    """
    Initializes the task's directory.
    """
    tasks_path = create_path_string(consts.TASKS_DIRECTORY)
    os.makedirs(tasks_path, exist_ok=True, mode=0o777)
