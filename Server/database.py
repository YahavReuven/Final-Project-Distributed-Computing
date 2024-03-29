"""
Module used to handle the database.
"""
import json
from dataclasses import asdict
from functools import wraps
from typing import Union

import consts
from consts import DatabaseType
from data_models import (Device, DeviceDB, Project, Task, Worker, ProjectStorage,
                         DB, DevicesDB, ProjectsDB, EncodedDevicesDB, TaskStatistics,
                         TaskStatisticsServer)
from utils import create_path_string, parse_timedelta
from handle_db_file_conversion import str_to_date_time, encode_json_recursively


def singleton(cls):
    """An implementation of singleton using decorator."""
    _instances = {}

    @wraps(cls)
    def wrapper(*args, **kwargs):
        if cls.__name__ not in _instances:
            _instances[cls.__name__] = cls(*args, **kwargs)
        return _instances[cls.__name__]

    return wrapper


class CustomEncoder(json.JSONEncoder):
    """Custom class to encode client in order to dump to json file."""

    def default(self, obj: object):
        """ Called in case json can't serialize object. """
        x = encode_json_recursively(asdict(obj))
        return x


class CustomDecoder(json.JSONDecoder):
    def __init__(self):
        super().__init__(object_hook=self.dict_to_object)

    @staticmethod
    def dict_to_object(obj: object):
        """ Called for every json object. """
        # NOTE: json decoder decodes from the inside outward.
        if isinstance(obj, dict):
            for key, val in obj.items():
                if isinstance(val, str):
                    try:
                        result = str_to_date_time(val)
                    except ValueError:
                        try:
                            result = parse_timedelta(val)
                        except ValueError:
                            result = val
                    finally:
                        obj[key] = result

        if isinstance(obj, dict) and 'devices' in obj:
            return EncodedDevicesDB(**obj)
        if isinstance(obj, dict) and 'device_id' in obj:
            return DeviceDB(**obj)
        if isinstance(obj, dict) and 'active_projects' in obj:
            return ProjectsDB(**obj)
        if isinstance(obj, dict) and 'project_id' in obj:
            return Project(**obj)
        if isinstance(obj, dict) and 'modules' in obj:
            return ProjectStorage(**obj)
        if isinstance(obj, dict) and 'workers' in obj:
            return Task(**obj)
        if isinstance(obj, dict) and 'worker_id' in obj:
            return Worker(**obj)
        if isinstance(obj, dict) and 'with_communications' in obj:
            return TaskStatisticsServer(**obj)
        if isinstance(obj, dict) and 'pure_run_time' in obj:
            return TaskStatistics(**obj)
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

    def init_devices_db(self, encoded_devices_db: EncodedDevicesDB):
        """
        Converts every device (DeviceDB) in the starting database to its
            Device representation.

        Args:
            encoded_devices_db (EncodedDevicesDB): the encoded devices' database.

        """
        self._db.devices_db = DBUtils.encoded_devices_db_to_devices_db(encoded_devices_db, self)

    def update_db(self):
        """
        Updates the database backup files.
        """
        devices_database_file = create_path_string(consts.DEVICES_DIRECTORY,
                                                   consts.DEVICES_DATABASE_NAME)
        with open(devices_database_file, 'w') as file:
            json.dump(self._db.devices_db, file, cls=CustomEncoder)
        projects_database_file = create_path_string(consts.PROJECTS_DIRECTORY,
                                                    consts.PROJECTS_DATABASE_NAME)
        with open(projects_database_file, 'w') as file:
            json.dump(self._db.projects_db, file, cls=CustomEncoder)

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

        if database_type & DatabaseType.devices_db and \
                database_type & DatabaseType.projects_db:
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
        """
        Adds a project or a device to the database.

        Args:
            obj (Union[Device, Project]): the object to add.
            database_type (DatabaseType): the part of the database to add the object to.

        """
        if database_type & DatabaseType.devices_db:
            self.get_database(DatabaseType.devices_db)[0].append(obj)
        if database_type & DatabaseType.active_projects_db:
            self.get_database(DatabaseType.active_projects_db)[0].append(obj)
        if database_type & DatabaseType.finished_projects_db:
            self.get_database(DatabaseType.finished_projects_db)[0].append(obj)
        if database_type & DatabaseType.waiting_to_return_projects_db:
            self.get_database(DatabaseType.waiting_to_return_projects_db)[0].append(obj)

    def remove_from_database(self, obj: Project, database_type: DatabaseType) -> bool:
        """
        Removes a project from the database.

        Args:
            obj (Project): the object to add.
            database_type (DatabaseType): the part of the database to add the object to.

        Returns:
            bool: whether the removal was successful.

        """
        if database_type & DatabaseType.active_projects_db:
            self.get_database(DatabaseType.active_projects_db)[0].remove(obj)
            return True
        if database_type & DatabaseType.waiting_to_return_projects_db:
            self.get_database(DatabaseType.waiting_to_return_projects_db)[0].remove(obj)
            return True
        return False

    def move_project(self, project: Project, move_from: DatabaseType,
                     move_to: DatabaseType):
        """
        Moves a project to a different part of the database.

        Args:
            project (Project): the project to move.
            move_from (DatabaseType): where is the project now.
            move_to (DatabaseType): where to move the project to.

        """
        self.add_to_database(project, move_to)
        self.remove_from_database(project, move_from)


class DBUtils:

    @staticmethod
    def encoded_devices_db_to_devices_db(encoded_device_db: Union[EncodedDevicesDB, dict],
                                         db: DBHandler, *, from_dict: bool = False) -> DevicesDB:
        """
        Converts every device (DeviceDB) in the starting database to its
            Device representation.

        Args:
            encoded_device_db (Union[EncodedDevicesDB, dict]): the encoded devices' database.
            db (DBHandler): the database handler.
            from_dict (bool) = False: whether the database is passed as dict.

        Returns:
            DevicesDB: the database in the new representation.

        """
        if from_dict:
            encoded_device_db = EncodedDevicesDB(**encoded_device_db)
        devices = [DBUtils.device_db_to_device(device_db, db) for device_db in
                   encoded_device_db.devices]
        return DevicesDB(devices=devices)

    @staticmethod
    def device_db_to_device(device_db: Union[DeviceDB, dict], db: DBHandler, *,
                            from_dict: bool = False) -> Device:
        """
        Converts a DeviceDB object to a Device object.

        Args:
            device_db (Union[DeviceDB, dict]): a database representation of a device.
            db (DBHandler): the db handler which devices need to be converted.
            from_dict (bool) = False: whether the database is passed as dict.

        Returns:
            Device: a Device instance based on the device db.

        """
        if from_dict:
            device_db = DeviceDB(**device_db)
        device_id = device_db.device_id
        projects = [DBUtils.find_in_db(project_id, DatabaseType.projects_db, db)
                    for project_id in device_db.projects_ids]
        is_blocked = device_db.is_blocked
        return Device(device_id=device_id, projects=projects, is_blocked=is_blocked)

    @staticmethod
    def find_in_db(search_id: str, database_type: DatabaseType, db: DBHandler = None) \
            -> Union[Device, Project, None]:
        """
        Looks for the object with the given id in the database specified in database_type.

        Note:
             the database_type should never include a combination of DatabaseType.device_db
                and another value which is contained in DatabaseType.projects_db.
                i.e. the following command should never return True:
                (database_type & DatabaseType.devices_db and
                 database_type & DatabaseType.projects_db)
        Args:
            search_id (str): the id of the object to be returned.
            database_type (DatabaseType): the database type in which to look for the object.
            db (DBHandler) = None: an optional parameter which allows to pass the db object
                needed instead of creating it inside the function. used for first init
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
                if device.device_id == search_id:
                    return device

        if database_type & DatabaseType.projects_db:
            for sub_database in database:
                for project in sub_database:
                    if project.project_id == search_id:
                        return project

        return None
