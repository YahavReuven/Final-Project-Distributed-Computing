"""
Module used to update the database and load it to memory correctly.
"""
import json
from datetime import datetime, timedelta
from typing import Any
from dataclasses import asdict
from functools import wraps
from typing import Union

import consts
from consts import DatabaseType
from data_models import (Device, DeviceDB, Project, Task, Worker, ProjectStorage,
                         DB, DevicesDB, ProjectsDB, WorkerDB, TaskDB, ProjectDB,
                         EncodedProjectsDB, EncodedDevicesDB, TaskStatistics,
                         TaskStatisticsServer, ProjectStatisticsServer # EncodedDB
                         )
from utils import create_path_string
from handle_db_file_conversion import (projects_db_to_encoded_projects_db,
                                       project_to_project_db, task_to_task_db,
                                       worker_to_worker_db, datetime_to_str,
                                       str_to_date_time,
                                       device_to_device_db, devices_db_to_encoded_devices_db,
                                       # encoded_projects_db_to_projects_db,
                                       # project_db_to_project, task_db_to_task,
                                       worker_db_to_worker,
                                       task_statistics_to_task_statistics_db,
                                       task_statistics_db_to_task_statistics,
                                       task_statistics_server_db_to_task_statistics_server,
                                       task_statistics_server_to_task_statistics_server_db,
                                       project_statistics_server_as_dict)


def singleton(cls):
    """ An implementation of singleton using decorator. """
    _instances = {}

    @wraps(cls)
    def wrapper(*args, **kwargs):
        if cls.__name__ not in _instances:
            _instances[cls.__name__] = cls(*args, **kwargs)
        return _instances[cls.__name__]

    return wrapper


class CustomEncoder(json.JSONEncoder):
    """ Custom class to encode client in order to dump to json file. """

    def default(self, obj: object):  # -> dict[str, Union[str, list[str]], bool]:
        """ Called in case json can't serialize object. """
        # TODO: find a better way
        print('DUMP:', obj, type(obj))
        if isinstance(obj, DevicesDB):
            return devices_db_to_encoded_devices_db(obj, dict_form=True)
        if isinstance(obj, Device):
            return device_to_device_db(obj, dict_form=True)
        if isinstance(obj, ProjectsDB):
            return projects_db_to_encoded_projects_db(obj, dict_form=True)
        if isinstance(obj, Project):
            return project_to_project_db(obj, dict_form=True)
        if isinstance(obj, Task):
            return task_to_task_db(obj, dict_form=True)
        if isinstance(obj, Worker):
            return worker_to_worker_db(obj, dict_form=True)
        if isinstance(obj, ProjectStorage):
            return asdict(obj)
        if isinstance(obj, ProjectStatisticsServer):
            return project_statistics_server_as_dict(obj, dict_form=True)
        if isinstance(obj, TaskStatisticsServer):
            return task_ststistics_server_to_task_statistics_server_db(obj, dict_form=True)
        if isinstance(obj, TaskStatistics):
            return task_statistics_to_task_statistics_db(obj, dict_form=True)
        if isinstance(obj, datetime):
            return datetime_to_str(obj)
        if isinstance(obj, timedelta):
            return str(obj)
        return super().default(obj)


class CustomDecoder(json.JSONDecoder):
    def __init__(self):
        super().__init__(object_hook=self.dict_to_object)

    @staticmethod
    def dict_to_object(obj: object) -> Union[Device, Project, Task, Worker, Any]:
        """ Called for every json object. """
        # NOTE: json decoder decodes from the inside outward.
        print('LOAD:', obj)
        if isinstance(obj, dict) and 'devices' in obj:
            return EncodedDevicesDB(**obj)
        if isinstance(obj, dict) and 'device_id' in obj:
            return DeviceDB(**obj)

        if isinstance(obj, dict) and 'active_projects' in obj:
            return ProjectsDB(**obj)
        if isinstance(obj, dict) and 'project_id' in obj:
            obj.update({"upload_time": str_to_date_time(obj["upload_time"])})
            return Project(**obj)
        if isinstance(obj, dict) and 'modules' in obj:
            return ProjectStorage(**obj)
        if isinstance(obj, dict) and 'workers' in obj:
            return Task(**obj)
        if isinstance(obj, dict) and 'worker_id' in obj:
            return worker_db_to_worker(obj, from_dict=True)
        if isinstance(obj, dict) and 'with_communications' in obj:
            return task_statistics_server_db_to_task_statistics_server(obj, from_dict=True)
        if isinstance(obj, dict) and 'pure_run_time' in obj:
            return task_ststistics_db_to_task_statistics(obj, from_dict=True)
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
        projects_database_file = create_path_string(consts.PROJECTS_DIRECTORY,
                                                    consts.PROJECTS_DATABASE_NAME)
        with open(projects_database_file, 'r') as file:
            projects_db = json.load(file, cls=CustomDecoder)
        devices_database_file = create_path_string(consts.DEVICES_DIRECTORY,
                                                   consts.DEVICES_DATABASE_NAME)
        with open(devices_database_file, 'r') as file:
            devices_db = json.load(file, cls=CustomDecoder)

        self._db = DB(projects_db=projects_db)

        self.init_devices_db(devices_db)

        print('a')

    def init_devices_db(self, encoded_devices_db: EncodedDevicesDB):
        """
        Converts every device (DeviceDB) in the starting database to its Device representation.
        """
        self._db.devices_db = DBUtils.encoded_devices_db_to_devices_db(encoded_devices_db, self)

    def update_db(self) -> None:
        """
        Updates the database backup files.
        """
        print('updating db...')  # TODO: remove after testing
        devices_database_file = create_path_string(consts.DEVICES_DIRECTORY,
                                                   consts.DEVICES_DATABASE_NAME)
        with open(devices_database_file, 'w') as file:
            json.dump(self._db.devices_db, file, cls=CustomEncoder)
        projects_database_file = create_path_string(consts.PROJECTS_DIRECTORY,
                                                    consts.PROJECTS_DATABASE_NAME)
        with open(projects_database_file, 'w') as file:
            json.dump(self._db.projects_db, file, cls=CustomEncoder)

    # TODO: check annotations
    def get_database(self, database_type: DatabaseType) -> \
            Union[list[list[Device]], list[list[Project]], None]:
        """
        Returns the database sections as specified in the database_type.
        Args:
            database_type (DatabaseType): the database sections to be returned.

        Returns:
            Union[list[list[Device]], list[list[Project]]]: a list containing
            lists for every section of the database that is to be returned.
        """
        results = []

        # TODO: raise error
        if database_type & DatabaseType.devices_db and database_type & DatabaseType.projects_db:
            return None

        if database_type & DatabaseType.devices_db:
            results.append(self._db.devices_db.devices)
        if database_type & DatabaseType.active_projects_db:
            results.append(self._db.projects_db.active_projects)
        if database_type & DatabaseType.waiting_to_return_projects_db:
            results.append(self._db.projects_db.waiting_projects)
        if database_type & DatabaseType.finished_projects_db:
            results.append(self._db.projects_db.finished_projects)

        return results

    def add_to_database(self, obj: Union[Device, Project], database_type: DatabaseType):
        if database_type & DatabaseType.devices_db:
            self.get_database(DatabaseType.devices_db)[0].append(obj)
        if database_type & DatabaseType.active_projects_db:
            self.get_database(DatabaseType.active_projects_db)[0].append(obj)
        if database_type & DatabaseType.finished_projects_db:
            self.get_database(DatabaseType.finished_projects_db)[0].append(obj)
        if database_type & DatabaseType.waiting_to_return_projects_db:
            self.get_database(DatabaseType.waiting_to_return_projects_db)[0].append(obj)

    # TODO: check if return is needed
    # TODO: allow to remove a Device and project from finished projects
    def remove_from_database(self, obj: Union[Device, Project], database_type: DatabaseType) -> bool:

        # if isinstance(obj, Device):
        #     self._devices_db[consts.DEVICES_DATABASE_KEY].append(obj)
        #     return True
        if database_type & DatabaseType.active_projects_db:
            self.get_database(DatabaseType.active_projects_db)[0].remove(obj)
            return True
        if database_type & DatabaseType.waiting_to_return_projects_db:
            self.get_database(DatabaseType.waiting_to_return_projects_db)[0].remove(obj)
            return True
        return False

    # TODO: check if succeeded
    def move_project(self, project: Project, move_from: DatabaseType, move_to: DatabaseType):  # -> bool:
        self.add_to_database(project, move_to)
        self.remove_from_database(project, move_from)


# TODO: add sort devices, sort projects, sort projects in device

class DBUtils:
    # @staticmethod
    # def device_to_device_db(device: Device) -> DeviceDB:
    #     """
    #     Converts a Device object to a DeviceDB object.
    #
    #     Args:
    #         device (Device): a device.
    #
    #     Returns:
    #         DeviceDB: the device's database representation.
    #
    #     """
    #     device_id = device.device_id
    #     projects_ids = [project.project_id for project in device.projects]  # TODO: sort when a new project is uploaded
    #     return DeviceDB(device_id=device_id, projects_ids=projects_ids)

    @staticmethod
    def encoded_devices_db_to_devices_db(encoded_device_db: Union[EncodedDevicesDB, dict],
                                         db: DBHandler, *, from_dict=False) -> DevicesDB:
        if from_dict:
            encoded_device_db = EncodedDevicesDB(**encoded_device_db)
        devices = [DBUtils.device_db_to_device(device_db, db) for device_db in encoded_device_db.devices]
        return DevicesDB(devices=devices)


    @staticmethod
    def device_db_to_device(device_db: Union[DeviceDB, dict], db: DBHandler, *,
                            from_dict=False) -> Device:
        """
        Converts a DeviceDB object to a Device object.

        Args:
            device_db (DeviceDB): a database representation of a device.
            db (DBHandler): the db handler which devices need to be converted.

        Returns:
            Device: a Device instance based on the device db.

        """
        if from_dict:
            device_db = DeviceDB(**device_db)
        device_id = device_db.device_id
        # TODO: maybe change
        projects = [DBUtils.find_in_db(project_id, DatabaseType.projects_db, db)
                    for project_id in device_db.projects_ids]
        return Device(device_id=device_id, projects=projects)

    # TODO: maybe raise errors for db
    @staticmethod
    def find_in_db(id: str, database_type: DatabaseType, db: DBHandler = None) -> Union[Device, Project, None]:
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
            db (DBHandler) = None: an optional parameter which allows to pass the db object
                needed instead of creating it inside of the function. used for first init
                in order to prevent infinite recursion.

        Returns:
            Union[Device, Project]: the device or project with the corresponding id.
            None: when no object with the given id is present in the given DatabaseType.
        """
        if not db:
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
