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
from consts import DatabaseType
from data_models import Device, DeviceDB, Project, Task, Worker
from utils import create_path_string

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
        """
        Loads the database into memory.
        """

        devices_database_file = create_path_string(consts.DEVICES_DIRECTORY,
                                                   consts.DEVICES_DATABASE_NAME)
        with open(devices_database_file, 'r') as file:
            self._devices_db = json.load(file, cls=CustomDecoder)
        projects_database_file = create_path_string(consts.PROJECTS_DIRECTORY,
                                                    consts.PROJECTS_DATABASE_NAME)
        with open(projects_database_file, 'r') as file:
            self._projects_db = json.load(file, cls=CustomDecoder)

    def init_device_dbs_to_devices(self):
        """
        Converts every device (DeviceDB) in the starting database to its Device representation.
        """

        devices = self._devices_db[consts.DEVICES_DATABASE_KEY]
        for i in range(len(devices)):
            devices[i] = DBUtils.device_db_to_device(devices[i])

    def update_db(self) -> None:
        """
        Updates the database backup files.
        """

        print('updating db...')  # TODO: remove after testing
        devices_database_file = create_path_string(consts.DEVICES_DIRECTORY,
                                                   consts.DEVICES_DATABASE_NAME)
        with open(devices_database_file, 'w') as file:
            json.dump(self._devices_db, file, cls=CustomEncoder)
        projects_database_file = create_path_string(consts.PROJECTS_DIRECTORY,
                                                    consts.PROJECTS_DATABASE_NAME)
        with open(projects_database_file, 'w') as file:
            json.dump(self._projects_db, file, cls=CustomEncoder)

    # TODO: check annotations
    def get_database(self, database_type: DatabaseType) -> \
            Union[list[list[Device]], list[list[Project]]]:
        """
        Returns the database sections as specified in the database_type.
        Args:
            database_type (DatabaseType): the database sections to be returned.

        Returns:
            Union[list[list[Device]], list[list[Project]]]: a list containing
            lists for every section of the database that is to be returned.
        """
        results = list()

        # TODO: raise error
        if database_type & DatabaseType.devices_db and database_type & DatabaseType.projects_db:
            return None

        if database_type & DatabaseType.devices_db:
            results.append(self._devices_db[consts.DEVICES_DATABASE_KEY])
        if database_type & DatabaseType.active_projects_db:
            results.append(self._projects_db[consts.ACTIVE_PROJECTS_DB_KEY])
        if database_type & DatabaseType.waiting_to_return_projects_db:
            results.append(self._projects_db[consts.WAITING_TO_RETURN_PROJECTS_DB_KEY])
        if database_type & DatabaseType.finished_projects_db:
            results.append(self._projects_db[consts.FINISHED_PROJECTS_DB_KEY])

        return results


    def add_to_database(self, obj: Union[Device, Project], database_type: DatabaseType) -> None:
        if database_type == DatabaseType.devices_db:
            self.get_database(DatabaseType.devices_db)[0].append(obj)
        if database_type == DatabaseType.active_projects_db:
            self.get_database(DatabaseType.active_projects_db)[0].append(obj)
        if database_type == DatabaseType.finished_projects_db:
            self.get_database(DatabaseType.finished_projects_db)[0].append(obj)
        if database_type == DatabaseType.waiting_to_return_projects_db:
            self.get_database(DatabaseType.waiting_to_return_projects_db)[0].append(obj)

    # TODO: allow to remove a Device and project from finished projects
    def remove_from_database(self, obj: Union[Device, Project], database_type: DatabaseType) -> bool:

        # if isinstance(obj, Device):
        #     self._devices_db[consts.DEVICES_DATABASE_KEY].append(obj)
        #     return True
        if database_type == DatabaseType.active_projects_db:
            self.get_database(DatabaseType.active_projects_db)[0].remove(obj)
            return True
        if database_type == DatabaseType.waiting_to_return_projects_db:
            self.get_database(DatabaseType.waiting_to_return_projects_db)[0].remove(obj)
            return True
        return False

    # TODO: check if succeeded
    def move_project(self, project: Project, move_from: DatabaseType, move_to: DatabaseType ):  # -> bool:
        self.add_to_database(project, move_to)
        self.remove_from_database(project, move_from)


# TODO: add sort devices, sort projects, sort projects in device

class DBUtils:
    @staticmethod
    def device_to_device_db(device: Device) -> DeviceDB:
        """
        Converts a Device object to a DeviceDB object.

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
        Converts a DeviceDB object to a Device object.

        Args:
            device_db (DeviceDB): a database representation of a device.

        Returns:
            Device: a Device instance based on the device db.

        """

        device_id = device_db.device_id
        # TODO: maybe change
        projects = [DBUtils.find_in_db(project_id, DatabaseType.projects_db)
                    for project_id in device_db.projects_ids]
        return Device(device_id=device_id, projects=projects)


    @staticmethod
    def find_in_db(id: str, database_type: DatabaseType) -> Union[Device, Project, None]:
        """
        Looks for the object with the given id in the database specified in database_type.

        Note:
             the database_type should never include a combination of DatabaseType.device_db
             and another value which is contained in DatabaseType.projects_db.
             i.e. the following command should never return True:
                (database_type & DatabaseType.devices_db and database_type & DatabaseType.projects_db)
        Args:
            id (str): the id of the object to be returned.
            database_type (DatabaseType): the database type in which to look for the object.

        Returns:
            Union[Device, Project]: the device or project with the corresponding id.
            None: when no object with the given id is present in the given DatabaseType.
        """
        db = DBHandler()
        database = db.get_database(database_type)

        if database_type & DatabaseType.devices_db:
            for device in database[0]:
                if device.device_id == id:
                    return device

        if database_type & DatabaseType.projects_db:
            for sub_database in database:
                for project in sub_database:
                    if project.project_id == id:
                        return project

        return None

    # @staticmethod
    # def find_project(project_id: str, database_type: DatabaseType) -> Union[Project, None]:
    #     """
    #
    #     Args:
    #         project_id (str): the project's id of the desired project.
    #         database_type (ProjectsDatabaseType): the project's database
    #             fields in which to look for the project.
    #
    #     Returns:
    #         Project: the project with the specified project id.
    #         None: if no project has the specified project id.
    #
    #     """
    #
    #     db = DBHandler()
    #     if database_type == ProjectsDatabaseType.all:
    #         result = DBUtils.find_project(project_id, ProjectsDatabaseType.active_projects_db)
    #         if not result:
    #             result = DBUtils.find_project(project_id, ProjectsDatabaseType.finished_projects_db)
    #         return result
    #     if database_type == ProjectsDatabaseType.active_projects_db:
    #         projects = db.get_database(DatabaseType.active_projects_db)
    #     else:
    #         projects = db.get_database(DatabaseType.finished_projects_db)
    #
    #     for project in projects:
    #         if project.project_id == project_id:
    #             return project
    #     return None
    #
    # @staticmethod
    # def find_project_in_multiple_db(project_id: str, database_types: list[ProjectsDatabaseType]):
    #     for database_type in database_types:
    #         if project := DBUtils.find_project(project_id, database_type):
    #             return project
    #     return None
    #
    # @staticmethod
    # def find_device(device_id: str) -> Union[Device, None]:
    #     """
    #
    #     Args:
    #         device_id (str): the device's id of the desired device.
    #
    #     Returns:
    #         Device: the device with the specified device id.
    #         None: if no project has the specified device id.
    #
    #     """
    #
    #     db = DBHandler()
    #     devices = db.get_database(DatabaseType.devices_db)
    #     for device in devices:
    #         if device.device_id == device_id:
    #             return device
    #     return None
