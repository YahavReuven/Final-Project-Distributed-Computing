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
from data_models import (Device, DeviceDB, Project, Task, Worker, ProjectStorage,
                         DB, DevicesDB, ProjectsDB, WorkerDB, TaskDB, ProjectDB,
                         EncodedProjectsDB, EncodedDevicesDB)
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
        # TODO: move to seperate file
        print(obj, type(obj))
        if isinstance(obj, DevicesDB):
            devices = []
            for device in obj.devices:
                devices.append(DBUtils.device_to_device_db(device))
            # TODO: find a better way which doesnt include literal strings
            encoded_devices_db = EncodedDevicesDB(devices=devices)
            return asdict(encoded_devices_db)
        # TODO: move to seperate file
        # TODO: find a better way
        if isinstance(obj, ProjectsDB):
            active = []
            waiting = []
            finished = []
            for project in obj.active_projects:
                active.append(self.default(project))
            for project in obj.waiting_projects:
                waiting.append(self.default(project))
            for project in obj.finished_projects:
                finished.append(self.default(project))
            encoded_projects_db = EncodedProjectsDB(active_projects=active,
                                                    waiting_projects=waiting,
                                                    finished_projects=finished)
            return asdict(encoded_projects_db)
        # if isinstance(obj, Project):
        #     tasks_db = []
        #     for task in obj.tasks:
        #         workers_db = []
        #         for worker in task.workers:
        #             sent_date_str = worker.sent_date.strftime(consts.DATETIME_FORMAT)
        #             workers_db.append(WorkerDB(worker_id=worker.worker_id, sent_date_str=sent_date_str,
        #                                        is_finished=worker.is_finished))
        #         tasks_db.append(TaskDB(workers=workers_db))
        #     project_db = ProjectDB(project_id=obj.project_id, tasks=tasks_db,
        #                            stop_number=obj.stop_number,
        #                            stop_immediately=obj.stop_immediately)
        #     return asdict(project_db)
        if isinstance(obj, Project):
            tasks = []
            for task in obj.tasks:
                tasks.append(self.default(task))
            project_db = ProjectDB(project_id=obj.project_id, tasks=tasks,
                                   stop_number=obj.stop_number,
                                   stop_immediately=obj.stop_immediately)
            return asdict(project_db)
        if isinstance(obj, Task):
            workers = []
            for worker in obj.workers:
                workers.append(self.default(worker))
            task_db = TaskDB(workers=workers)
            return asdict(task_db)
        if isinstance(obj, Worker):
            sent_date_str = self.default(obj.sent_date)
            worker_db = WorkerDB(worker_id=obj.worker_id, sent_date=sent_date_str,
                                 is_finished=obj.is_finished)
            return asdict(worker_db)
        if isinstance(obj, ProjectStorage):
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
        if isinstance(obj, dict) and 'devices' in obj:
            return DevicesDB(**obj)
        if isinstance(obj, dict) and 'active_projects' in obj:
            temp_projects_db = EncodedProjectsDB(**obj)
            active = []
            waiting = []
            finished = []
            for project in temp_projects_db.active_projects:
                active.append(CustomDecoder.dict_to_object(project))
            for project in temp_projects_db.waiting_projects:
                waiting.append(CustomDecoder.dict_to_object(project))
            for project in temp_projects_db.finished_projects:
                finished.append(CustomDecoder.dict_to_object(project))
            projects_db = ProjectsDB(active_projects=active, waiting_projects=waiting,
                                     finished_projects=finished)
            return projects_db
        if isinstance(obj, dict) and 'device_id' in obj:
            return DeviceDB(**obj)
        if isinstance(obj, dict) and 'project_id' in obj:
            project_db = ProjectDB(**obj)
            tasks = []
            for task in project_db.tasks:
                tasks.append(CustomDecoder.dict_to_object(task))
            project = Project(project_id=project_db.project_id, tasks=tasks,
                              stop_number=project_db.stop_number,
                              stop_immediately=project_db.stop_immediately)
            return project
        if isinstance(obj, dict) and 'modules' in obj:
            return ProjectStorage(**obj)
        if isinstance(obj, dict) and 'workers' in obj:
            task_db = TaskDB(**obj)
            workers = []
            for worker in task_db.workers:
                workers.append(CustomDecoder.dict_to_object(worker))
            task = Task(workers=workers)
            return task
        if isinstance(obj, dict) and 'worker_id' in obj:
            worker_db = WorkerDB(**obj)
            sent_date = datetime.strptime(
                worker_db.sent_date, consts.DATETIME_FORMAT)
            worker = Worker(worker_id=worker_db.worker_id, sent_date=sent_date,
                            is_finished=worker_db.is_finished)
            return worker
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
            devices_db = json.load(file, cls=CustomDecoder)
        projects_database_file = create_path_string(consts.PROJECTS_DIRECTORY,
                                                    consts.PROJECTS_DATABASE_NAME)
        with open(projects_database_file, 'r') as file:
            projects_db = json.load(file, cls=CustomDecoder)
        self._db = DB(devices_db=devices_db, projects_db=projects_db)
        print('a')

    def init_device_dbs_to_devices(self):
        """
        Converts every device (DeviceDB) in the starting database to its Device representation.
        """
        devices = self._db.devices_db.devices
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
