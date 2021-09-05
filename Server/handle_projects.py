# TODO: module needs checking ang changing
"""
Module used to handle projects and the projects' database
"""
import base64
import json
from uuid import uuid4
from typing import Union

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
    validate_base64_and_decode(new_project.base64_serialized_class)
    validate_base64_and_decode(new_project.base64_serialized_iterable)

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


async def return_project_results(device_id: str, project_id: str) -> ReturnedProject:
    # authenticate device and project id
    # merge results to json file
    # zip the additional results
    # remove files
    #
    #

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

    return returned_project


def store_serialized_project(project: NewProject, project_id: str):
    """
    Stores the project's code (class) and iterable.

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
                        project.base64_serialized_iterable}
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


# TODO: not sure that is needed
def encode_zipped_project(project_id: str) -> bytes:
    zipped_project_path = create_path_string(consts.PROJECTS_DIRECTORY, project_id,
                                             consts.PROJECT_STORAGE_PROJECT,
                                             consts.PROJECT_STORAGE_JSON_PROJECT)

    with open(zipped_project_path, 'rb') as file:
        zipped_project = file.read()

    encoded_project = base64.b64encode(zipped_project)

    return encoded_project
