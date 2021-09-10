"""
Module used to handle the data of the users.
"""

import json
from functools import wraps
import ipaddress

from handle_requests import request_register_device
from utils import create_path_string
import consts
from errors import InvalidIPv4Address, InvalidPortNumber
from users_utils import get_users_names

from uuid import uuid4

# TODO: add costume json encoder and decoder

# TODO: check for a better way
def name_based_singleton(cls):
    """
    An implementation of a name based singleton using decorator.

    Note:
        The purpose of this function is to allow the creation of
        a UsersDataHandler instance only if an instance with the same
        name isn't already created.
        This is a helper function for the UsersDataHandler class and
        should receive only this class.

    Args:
        cls (UsersDataHandler): the UsersDataHandler class

    Returns:
        function: a decorator.
    """
    _instances = {}

    @wraps(cls)
    def wrapper(user_name):
        instance = _instances.get(user_name)
        # _instances.setdefault(user_name, cls(user_name))
        if not instance:
            instance = cls(user_name)
            _instances[user_name] = instance
        return instance

    return wrapper


@name_based_singleton
class UsersDataHandler:

    def __init__(self, user_name):
        self.user_name = user_name

        try:
            self._load_data()
        except FileNotFoundError:
            # TODO: change to gui
            server_ip = input("please enter the server's ip:")
            server_port = input("please enter the port number:")

            self._set_device_id()
            print(user_name, self.device_id)
            self._config_new_user(server_ip, server_port, self.device_id)
            self._update_data_file()

    @property
    def ip(self):
        return self._ip

    @property
    def port(self):
        return self._port

    @property
    def device_id(self):
        return self._device_id

    @property
    def projects(self):
        return self._projects

    @property
    def tasks(self):
        return self._tasks

    def _config_new_user(self, server_ip, server_port, device_id):
        """
        Configures the new user.
        """
        self._validate_new_user(server_ip, server_port)
        self._ip = server_ip
        self._port = server_port
        self._device_id = device_id
        self._projects = []
        self._tasks = []

    @staticmethod
    def _validate_new_user(server_ip, server_port):
        """
        Validates the user's data.
        """
        try:
            ipaddress.ip_address(server_ip)
        except ValueError:
            raise InvalidIPv4Address

        # TODO: check condition
        if not (server_port.isdigit() and
                consts.MIN_PORT_NUM <= int(server_port) <= consts.MAX_PORT_NUM):
            raise InvalidPortNumber

    def _load_data(self):
        """
        Loads the user's data from its file.
        """
        data_file_path = create_path_string(consts.USERS_DIRECTORY,
                                            self.user_name + consts.JSON_EXTENSION)

        with open(data_file_path, 'r') as file:
            data = json.load(file)
            self._ip = data[consts.USER_IP_KEY]
            self._port = data[consts.USER_PORT_KEY]
            self._device_id = data[consts.USER_DEVICE_ID_KEY]
            self._projects = data[consts.USER_PROJECTS_KEY]
            self._tasks = data[consts.USER_TASKS_KEY]

    def _update_data_file(self):
        """
        Updates the user's data file.
        """
        data_file_path = create_path_string(consts.USERS_DIRECTORY,
                                            self.user_name + consts.JSON_EXTENSION)

        data = {consts.USER_IP_KEY: self._ip,
                consts.USER_PORT_KEY: self._port,
                consts.USER_DEVICE_ID_KEY: self._device_id,
                consts.USER_PROJECTS_KEY: self._projects,
                consts.USER_TASKS_KEY: self._tasks}

        with open(data_file_path, 'w') as file:
            json.dump(data, file)

    def _set_device_id(self):
        names = get_users_names()
        for name in names:
            user = UsersDataHandler(name)
            if user.ip == self.ip and user.port == self.port:
                self._device_id = user.device_id
                return

        self._device_id = uuid4().hex  # request_register_device(server_ip, server_port)

    def add_task(self):
        pass
