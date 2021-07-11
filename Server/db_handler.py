import json
from typing import Union, Any
from dataclasses import asdict
from functools import wraps

import consts
from consts import Device, DeviceDB, Project

def singleton(cls):
    """ An implementation of singleton using decorator. """
    _instances = {}

    @wraps(cls)
    def wrapper(*args, **kwargs):
        return _instances.setdefault(cls.__name__, cls(*args, **kwargs))

    return wrapper


class CustomEncoder(json.JSONEncoder):
    """ Custom class to encode client in order to dump to json file. """

    def default(self, obj: object) -> dict[str, Union[str, list[str]], bool]:
        """ Called in case json can't serialize object. """
        if isinstance(obj, Device):
            return asdict(device_to_device_db(obj))
        if isinstance(obj, Project):
            return asdict(obj)
        return json.JSONEncoder.default(self, obj)


class CustomDecoder(json.JSONDecoder):
    def __init__(self):
        super().__init__(object_hook=self.dict_to_object)

    @staticmethod
    def dict_to_object(obj: object) -> Union[Device, Any]:
        """ Called for every json object. """
        if isinstance(obj, dict) and 'device_id' in obj:
            return device_db_to_device()
        if isinstance(obj, dict) and 'tasks' in obj:
            return Project(**obj)
        return obj


@singleton
class DBHandler:
    """ Class to handle DB related tasks. """

    def __init__(self):
        self._load_db()

    def _load_db(self) -> None:
        with open(consts.DEVICES_DATABASE_NAME, 'r') as file:
            self._devices_db = json.load(file, cls=CustomDecoder)
        with open(consts.PROJECTS_DATABASE_NAME, 'r') as file:
            self._projects_db = json.load(file, cls=CustomDecoder)

    def update_db(self) -> None:
        print('updating db...')
        with open(consts.DEVICES_DATABASE_NAME, 'w') as file:
            json.dump(self._devices_db, file, cls=CustomEncoder)
        with open(consts.PROJECTS_DATABASE_NAME, 'w') as file:
            json.dump(self._projects_db, file, cls=CustomEncoder)

    @property
    def devices_db(self) -> dict[str, list[Device]]:
        return self._devices_db

    @property
    def projects_db(self) -> dict[str, list[Project]]:
        return self._projects_db


def device_to_device_db(device: Device) -> DeviceDB:
    """

    Args:
        device (Device): a device.

    Returns:
        DeviceDB: the device's database representation.

    """
    device_id = device.device_id
    projects_ids = sorted([project.project_id for project in device.projects])  # TODO: sort when a new project is uploaded
    return DeviceDB(device_id=device_id, projects_ids=projects_ids)


def device_db_to_device(device_db: DeviceDB) -> Device:
    """

    Args:
        device_db (DeviceDB): a database representation of a device.

    Returns:
        Device: a Device instance based on the device db.

    """

    device_id = device_db.device_id
    projects = [find_project(project_id) for project_id in DeviceDB.projects_ids]
    return Device(device_id=device_id, projects=projects)

def find_project(project_id: str) -> Union[Project, None]:

    """

    Args:
        project_id (str): the project's id of the desired project.

    Returns:
        Project: the project with the specified project id.
        None: if no project has the specified project id.

    """

    db = DBHandler()
    projects = db.projects_db[consts.PROJECTS_DATABASE_KEY]
    for project in projects:
        if project.project_id == project_id:
            return project
    return None