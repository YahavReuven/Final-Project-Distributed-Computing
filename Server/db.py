"""
Module used to update the database and load it to memory correctly.
"""
import json
from datetime import datetime
from typing import Any
from dataclasses import asdict
from functools import wraps
from typing import Union

import consts
from consts import DatabaseType, ProjectsDatabaseType
from data_models import Device, DeviceDB, Project, Task, Worker


def singleton(cls):
    """ An implementation of singleton using decorator. """
    _instances = {}

    @wraps(cls)
    def wrapper(*args, **kwargs):
        return _instances.setdefault(cls.__name__, cls(*args, **kwargs))

    return wrapper


class CustomEncoder(json.JSONEncoder):
    """ Custom class to encode client in order to dump to json file. """

    def default(self, obj: object):  # -> dict[str, Union[str, list[str]], bool]:
        """ Called in case json can't serialize object. """
        if isinstance(obj, Device):
            return asdict(DBUtils.device_to_device_db(obj))
        if isinstance(obj, (Project, Task, Worker)):
            return asdict(obj)
        if isinstance(obj, datetime):
            return obj.strftime(consts.DATETIME_FORMAT)
        return super().default(obj)


class CustomDecoder(json.JSONDecoder):
    def __init__(self):
        super().__init__(object_hook=self.dict_to_object)

    @staticmethod
    def dict_to_object(obj: object) -> Union[Device, Project, Task, Worker, Any]:
        """ Called for every json object. """
        if isinstance(obj, dict) and 'device_id' in obj:
            return DeviceDB(**obj)
        if isinstance(obj, dict) and 'project_id' in obj:
            return Project(**obj)
        if isinstance(obj, dict) and 'workers_ids' in obj:
            return Task(**obj)
        if isinstance(obj, dict) and 'worker_id' in obj:
            obj[consts.SENT_TASK_DATE_KEY] = datetime.strptime(
                obj[consts.SENT_TASK_DATE_KEY], consts.DATETIME_FORMAT)
            return Worker(**obj)
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

    def init_device_dbs_to_devices(self):
        devices = self._devices_db[consts.DEVICES_DATABASE_KEY]
        for i in range(len(devices)):
            devices[i] = DBUtils.device_db_to_device(devices[i])

    def update_db(self) -> None:
        print('updating db...')  # TODO: remove after testing
        with open(consts.DEVICES_DATABASE_NAME, 'w') as file:
            json.dump(self._devices_db, file, cls=CustomEncoder)
        with open(consts.PROJECTS_DATABASE_NAME, 'w') as file:
            json.dump(self._projects_db, file, cls=CustomEncoder)

    def get_database(self, database_type: DatabaseType) -> \
            Union[list[Device], list[Project]]:
        if database_type == DatabaseType.devices_db:
            return self._devices_db[consts.DEVICES_DATABASE_KEY]
        if database_type == DatabaseType.projects_db:
            return self._projects_db[consts.PROJECTS_DATABASE_KEY]
        if database_type == DatabaseType.finished_projects_db:
            return self._projects_db[consts.FINISHED_PROJECTS_DATABASE_KEY]

    def add_to_database(self, obj: Union[Device, Project], database_type: DatabaseType) -> None:
        if database_type == DatabaseType.devices_db:
            self.get_database(DatabaseType.devices_db).append(obj)
        if database_type == DatabaseType.projects_db:
            self.get_database(DatabaseType.projects_db).append(obj)
        if database_type == DatabaseType.finished_projects_db:
            self.get_database(DatabaseType.finished_projects_db).append(obj)

    # TODO: allow to remove a Device and project from finished projects
    def remove_from_database(self, obj: Union[Device, Project], database_type: DatabaseType) -> bool:

        # if isinstance(obj, Device):
        #     self._devices_db[consts.DEVICES_DATABASE_KEY].append(obj)
        #     return True
        if database_type == DatabaseType.projects_db:
            self.get_database(DatabaseType.projects_db).remove(obj)
            return True
        return False

    # TODO: check if succeeded
    def move_project_to_finished(self, project: Project):  # -> bool:
        self.add_to_database(project, DatabaseType.finished_projects_db)
        self.remove_from_database(project, DatabaseType.projects_db)


# TODO: add sort devices, sort projects, sort projects in device

class DBUtils:
    @staticmethod
    def device_to_device_db(device: Device) -> DeviceDB:
        """

        Args:
            device (Device): a device.

        Returns:
            DeviceDB: the device's database representation.

        """
        device_id = device.device_id
        projects_ids = [project.project_id for project in device.projects]  # TODO: sort when a new project is uploaded
        return DeviceDB(device_id=device_id, projects_ids=projects_ids)

    @staticmethod
    def device_db_to_device(device_db: DeviceDB) -> Device:
        """

        Args:
            device_db (DeviceDB): a database representation of a device.

        Returns:
            Device: a Device instance based on the device db.

        """

        device_id = device_db.device_id
        projects = [DBUtils.find_project(project_id, ProjectsDatabaseType.both)
                    for project_id in device_db.projects_ids]
        return Device(device_id=device_id, projects=projects)

    @staticmethod
    def find_project(project_id: str, database_type: ProjectsDatabaseType) -> Union[Project, None]:
        """

        Args:
            project_id (str): the project's id of the desired project.
            database_type (ProjectsDatabaseType): the project's database
                fields in which to look for the project.

        Returns:
            Project: the project with the specified project id.
            None: if no project has the specified project id.

        """

        db = DBHandler()
        if database_type == ProjectsDatabaseType.both:
            result = DBUtils.find_project(project_id, ProjectsDatabaseType.projects_db)
            if not result:
                result = DBUtils.find_project(project_id, ProjectsDatabaseType.finished_projects_db)
            return result
        if database_type == ProjectsDatabaseType.projects_db:
            projects = db.get_database(DatabaseType.projects_db)
        else:
            projects = db.get_database(DatabaseType.finished_projects_db)

        for project in projects:
            if project.project_id == project_id:
                return project
        return None

    @staticmethod
    def find_device(device_id: str) -> Union[Device, None]:
        """

        Args:
            device_id (str): the device's id of the desired device.

        Returns:
            Device: the device with the specified device id.
            None: if no project has the specified device id.

        """

        db = DBHandler()
        devices = db.get_database(DatabaseType.devices_db)
        for device in devices:
            if device.device_id == device_id:
                return device
        return None