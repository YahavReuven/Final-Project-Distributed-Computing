"""
Module used to handle the users.
"""


def create_new_user():
    pass


def get_user():
    pass



class User:
    """
    A class which handles the user's data.
    """

    def __init__(self, user_name, server_ip, server_port, device_id, projects = [], tasks = []):
        self.user_name = user_name
        self.server_ip = server_ip
        self.server_port = server_port
        self.device_id = device_id
        self.projects = projects
        self.tasks = tasks

    def _update_data_file(self):
        pass

    def add_task(self):
        pass



