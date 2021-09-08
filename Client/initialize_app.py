"""
Module used to initialize the application.
"""

import os

from utils import create_path_string
import consts
from handle_users_data import UsersDataHandler


# def create_new_user(user_name):
#     self._validate_new_user(server_ip, server_port)
#     server_ip = input("please enter the server's ip:")
#     server_port = input("please enter the port number:")
#     device_id = request_register_device(server_ip, server_port)
#     self.ip = server_ip
#     self.port = server_port
#     self.device_id = device_id
#     self.projects = []
#     self.tasks = []


def init_user():
    users_path = create_path_string(consts.USERS_DIRECTORY)
    os.makedirs(users_path, exist_ok=True)

    user_name = input('please enter the user name: ')
    return UsersDataHandler(user_name)


def init_tasks():
    tasks_path = create_path_string(consts.TASKS_DIRECTORY)
    os.makedirs(tasks_path, exist_ok=True)


