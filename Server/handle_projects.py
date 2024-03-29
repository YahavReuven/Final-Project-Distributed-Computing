"""
Module used to handle projects and the projects' database.
"""
import json
import os
from uuid import uuid4
import shutil
from datetime import datetime

import consts
from consts import DatabaseType
from data_models import Project, NewProject, ReturnedProject, ProjectStorage
from errors import (DeviceNotFoundError, ProjectNotFoundError, ProjectIsActive,
                    ProjectFinishedError)
from database import DBHandler, DBUtils, CustomEncoder
from initialize_server import init_project_storage
from storage_handler import merge_results, zip_additional_results
from authentication import authenticate_creator
from utils import (create_path_string, validate_base64_and_decode,
                   rmtree_onerror_remove_readonly)
from server_statistics import create_project_statistics


async def create_new_project(new_project: NewProject) -> str:
    """
    Creates a new project, initializes its storage and updates the database.

    Args:
        new_project (NewProject): contains the needed information about
            the uploaded project.

    Returns:
        str: the project's id.

    Raises:
        DeviceNotFoundError: if the received NewProject contains a creator
            id which is not present in the database.
        InvalidBase64Error: if the received NewProject contains an invalid base64.

    """
    if not (creator := DBUtils.find_in_db(new_project.creator_id,
                                          DatabaseType.devices_db)):
        raise DeviceNotFoundError
    validate_base64_and_decode(new_project.base64_serialized_class, return_obj=False)
    validate_base64_and_decode(new_project.base64_serialized_iterable, return_obj=False)

    project_id = uuid4().hex
    init_project_storage(project_id)
    store_serialized_project(new_project, project_id)
    upload_project_time = datetime.utcnow()
    project = Project(project_id=project_id, upload_time=upload_project_time)

    db = DBHandler()
    db.add_to_database(project, DatabaseType.active_projects_db)
    creator.projects.append(project)

    return project_id


async def return_project_results(device_id: str, project_id: str) -> ReturnedProject:
    """
    Returns a project's results.

    Args:
        device_id (str): the device id of the client requesting the results.
        project_id (str): the project id of the project that its results
            are requested.

    Returns:
        ReturnedProject: the results of the project.

    Raises:
        ProjectIsActive: if the project is still active.
        ProjectFinishedError: if the results of a project are requested
            more than once.
        ProjectNotFoundError: if the project is not found.

    """
    authenticate_creator(device_id, project_id)
    project, project_state = get_project_state(project_id)
    if project_state & DatabaseType.active_projects_db:
        raise ProjectIsActive
    if project_state & DatabaseType.finished_projects_db:
        raise ProjectFinishedError
    if not project_state:
        raise ProjectNotFoundError

    results = merge_results(project_id)
    additional_results = zip_additional_results(project_id)
    statistics = json.dumps(create_project_statistics(project_id), cls=CustomEncoder)
    returned_project = ReturnedProject(results=results,
                                       base64_zipped_additional_results=additional_results,
                                       statistics=statistics)

    db = DBHandler()
    db.move_project(project, DatabaseType.waiting_to_return_projects_db,
                    DatabaseType.finished_projects_db)

    delete_finished_project_storage(project)

    return returned_project


def store_serialized_project(project: NewProject, project_id: str):
    """
    Stores the project's code (class), iterator and task size.

    Note:
        Assumes that the project's storage is already initialized.
        Assumes that the given base64 data is valid.

    Args:
        project (NewProject): the project which needs to be stored.
        project_id (str): the project's id.

    """
    serialized_project_path = create_path_string(consts.PROJECTS_DIRECTORY, project_id,
                                                 consts.PROJECT_STORAGE_PROJECT,
                                                 consts.PROJECT_STORAGE_JSON_PROJECT)
    project_storage = ProjectStorage(base64_serialized_class=
                                     project.base64_serialized_class,
                                     base64_serialized_iterable=
                                     project.base64_serialized_iterable,
                                     modules=project.modules,
                                     task_size=project.task_size,
                                     parallel_func=project.parallel_func,
                                     stop_func=project.stop_func,
                                     only_if_func=project.only_if_func
                                     )

    with open(serialized_project_path, 'w') as file:
        os.chmod(serialized_project_path, mode=0o777)
        json.dump(project_storage, file, cls=CustomEncoder)


def is_project_done(project: Project) -> bool:
    """
    Checks whether a project is done.

    Args:
        project (Project): the project needed checking.

    Returns:
        bool: whether the project is done.

    """
    if project.stop_immediately:
        return True

    if project.stop_number >= 0:
        for i in range(project.stop_number):
            for worker in project.tasks[i].workers:
                if not worker.is_finished:
                    return False
        return True

    return False


def get_project_state(project_id: str):
    """
    Checks the project's state.

    Args:
        project_id (str): the id of the project.

    Returns:
        the project and its state.

    """
    if project := DBUtils.find_in_db(project_id, DatabaseType.active_projects_db):
        return project, DatabaseType.active_projects_db
    if project := DBUtils.find_in_db(project_id, DatabaseType.waiting_to_return_projects_db):
        return project, DatabaseType.waiting_to_return_projects_db
    if project := DBUtils.find_in_db(project_id, DatabaseType.finished_projects_db):
        return project, DatabaseType.finished_projects_db

    return None, None


def delete_finished_project_storage(project: Project):
    """
    Deletes the storage of a finished project.

    Args:
        project (Project): the project that its storage is to be deleted.

    """
    project_path = create_path_string(consts.PROJECTS_DIRECTORY, project.project_id)
    shutil.rmtree(project_path, onerror=rmtree_onerror_remove_readonly)
