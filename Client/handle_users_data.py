"""
Module used to handle the data of the users.
"""
import json
from functools import wraps
import ipaddress

import consts
from handle_requests import request_register_device
from utils import create_path_string
from errors import InvalidIPv4Address, InvalidPortNumber
from users_utils import get_users_names
from data_models import User, StorageTaskStatistics, TaskStatistics
from handle_json import CustomDecoder, CustomEncoder


def name_based_singleton(cls):
    """
    An implementation of a name based singleton using decorator.

    Note:
        The purpose of this function is to allow the creation of
            a UsersDataHandler instance only if an instance (a user)
            with the same user name isn't already created.
        This is a helper function for the UsersDataHandler class and
            should receive only this class.

    Args:
        cls (UsersDataHandler): the UsersDataHandler class.

    Returns:
        function: a decorator.

    """
    _instances = {}

    @wraps(cls)
    def wrapper(user_name):
        instance = _instances.get(user_name)
        if not instance:
            instance = cls(user_name)
            _instances[user_name] = instance
        return instance

    return wrapper


@name_based_singleton
class UsersDataHandler:

    def __init__(self, user_name: str):
        self._user_name = user_name

        try:
            self._load_data()
        except FileNotFoundError:
            self._create_new_user()

    @property
    def user(self):
        return self._user

    def _create_new_user(self):
        """
        Creates a new user.
        """
        server_ip = input("please enter the server's ip: ")
        server_port = input("please enter the port number: ")

        self._validate_new_user(server_ip, server_port)
        server_port = int(server_port)

        device_id = self._set_device_id(server_ip, server_port)
        self._user = User(ip=server_ip, port=server_port, device_id=device_id)
        self._update_data_file()

    @staticmethod
    def _validate_new_user(server_ip: str, server_port: str):
        """
        Validates the user's data.

        Args:
            server_ip (str): the ip of the server.
            server_port (str): the port of the server.

        Raises:
            InvalidIPv4Address: if an invalid ip address was passed.
            InvalidPortNumber: if an invalid port number was passed.

        """
        try:
            ipaddress.ip_address(server_ip)
        except ValueError:
            raise InvalidIPv4Address

        if not (server_port.isdigit() and
                consts.MIN_PORT_NUM <= int(server_port) <= consts.MAX_PORT_NUM):
            raise InvalidPortNumber

    def _load_data(self):
        """
        Loads the user's data from its file.
        """
        data_file_path = create_path_string(consts.USERS_DIRECTORY,
                                            self._user_name + consts.JSON_EXTENSION)
        with open(data_file_path, 'r') as file:
            self._user = json.load(file, cls=CustomDecoder)

    def _update_data_file(self):
        """
        Updates the user's data file.
        """
        data_file_path = create_path_string(consts.USERS_DIRECTORY,
                                            self._user_name + consts.JSON_EXTENSION)

        with open(data_file_path, 'w') as file:
            json.dump(self.user, file, cls=CustomEncoder)

    def _set_device_id(self, ip: str, port: int):
        """
        Sets the device id of the user.

        Args:
            ip (str): the ip of the server.
            port (int): the port of the server.

        Returns:
            str: the device id.

        """
        names = get_users_names()
        for name in names:
            user = UsersDataHandler(name)
            if user.user.ip == ip and user.user.port == port:
                return user.user.device_id
        return request_register_device(ip, port)

    def add_task(self, project_id: str, task_number: int, task_statistics: TaskStatistics):
        """
        Saves the statistics of a task.

        Args:
            project_id (str): the id ot the task's project.
            task_number (int): the number of the task.
            task_statistics (TaskStatistics): the statistics generated from the task.

        """
        statistics = StorageTaskStatistics(project_id=project_id, task_number=task_number,
                                           statistics=task_statistics)
        self._user.tasks.append(statistics)
        self._update_data_file()
