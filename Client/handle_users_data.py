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

        # TODO: change to gui
        server_ip = input("please enter the server's ip:")
        server_port = input("please enter the port number:")
        device_id = request_register_device(server_ip, server_port)
        print(user_name, device_id)
        self.config_new_user(server_ip, server_port, device_id)
        self._update_data_file()

    def config_new_user(self, server_ip, server_port, device_id):
        """
        Configures the new user.
        """
        self._validate_new_user(server_ip, server_port)
        self.ip = server_ip
        self.port = server_port
        self.device_id = device_id
        self.projects = []
        self.tasks = []


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
        data_file_path = create_path_string(consts.USERS_DIRECTORY, self.user_name,
                                            consts.JSON_EXTENSION)

        with open(data_file_path, 'r') as file:
            data = json.load(file)
            self.ip = data[consts.DATA_IP_KEY]
            self.port = data[consts.DATA_PORT_KEY]
            self.device_id = data[consts.DATA_DEVICE_ID_KEY]
            self.projects = data[consts.DATA_PROJECTS_KEY]
            self.tasks = data[consts.DATA_TASKS_KEY]

    def _update_data_file(self):
        """
        Updates the user's data file.
        """
        data_file_path = create_path_string(consts.USERS_DIRECTORY,
                                            self.user_name + consts.JSON_EXTENSION)

        data = {consts.DATA_IP_KEY: self.ip,
                consts.DATA_PORT_KEY: self.port,
                consts.DATA_DEVICE_ID_KEY: self.device_id,
                consts.DATA_PROJECTS_KEY: self.projects,
                consts.DATA_TASKS_KEY: self.tasks}

        with open(data_file_path, 'w') as file:
            json.dump(data, file)
