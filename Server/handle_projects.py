# TODO: module needs checking ang changing
"""
Module used to handle projects and the projects' database
"""
import json
from uuid import uuid4
import shutil

import consts
from consts import DatabaseType
from data_models import Project, NewProject, ReturnedProject
from errors import (DeviceNotFoundError, ProjectNotFoundError, ProjectIsActive,
                    ProjectFinishedError)
from db import DBHandler, DBUtils
from initialize_server import init_project_storage
from storage_handler import merge_results, zip_additional_results
from authentication import authenticate_creator
from utils import create_path_string, validate_base64_and_decode


# TODO: make it work with UploadFile instead of bytes
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
        InvalidBase64Error: if the received NewProject contains invalid base64.

    """
    validate_base64_and_decode(new_project.base64_serialized_class, return_obj=False)
    validate_base64_and_decode(new_project.base64_serialized_iterable, return_obj=False)

    project_id = uuid4().hex
    init_project_storage(project_id)
    store_serialized_project(new_project, project_id)

    project = Project(project_id=project_id)
    if not (creator := DBUtils.find_in_db(new_project.creator_id,
                                          DatabaseType.devices_db)):
        raise DeviceNotFoundError

    db = DBHandler()
    db.add_to_database(project, DatabaseType.active_projects_db)
    creator.projects.append(project)

    return project_id


# TODO: check annotation
# TODO: maybe remove the finished field in the database
async def return_project_results(device_id: str, project_id: str) -> ReturnedProject:
    """
    Returns a project results.

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

    returned_project = ReturnedProject(results=results, base64_zipped_additional_results=additional_results)

    db = DBHandler()
    db.move_project(project, DatabaseType.waiting_to_return_projects_db, DatabaseType.finished_projects_db)

    delete_finished_project_storage(project)

    return returned_project


# TODO: maybe change name
# TODO: change consts to dataclass
def store_serialized_project(project: NewProject, project_id: str):
    """
    Stores the project's code (class), iterable and task size.

    Note:
        Assumes that the project's storage is already  initialized.
        Assumes that the given base64 data is valid.

    Args:
        project (NewProject): the project which needs to be stored.
        project_id: the project's id of the project.

    """

    serialized_project_path = create_path_string(consts.PROJECTS_DIRECTORY, project_id,
                                                 consts.PROJECT_STORAGE_PROJECT,
                                                 consts.PROJECT_STORAGE_JSON_PROJECT)

    project_code = {consts.JSON_PROJECT_BASE64_SERIALIZED_CLASS:
                        project.base64_serialized_class,
                    consts.JSON_PROJECT_BASE64_SERIALIZED_ITERABLE:
                        project.base64_serialized_iterable,
                    consts.JSON_PROJECT_MODULES: project.modules,
                    consts.JSON_PROJECT_TASK_SIZE: project.task_size}
    with open(serialized_project_path, 'w') as file:
        json.dump(project_code, file)


def is_project_done(project: Project) -> bool:
    if project.stop_immediately:
        return True

    if project.stop_number >= 0:
        for i in range(project.stop_number):
            for worker in project.tasks[i].workers:
                if not worker.is_finished:
                    return False
        return True

    return False


def get_project_state(project_id: str):  # -> Union[(Project, DatabaseType), (None, None)]:
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
    shutil.rmtree(project_path)
