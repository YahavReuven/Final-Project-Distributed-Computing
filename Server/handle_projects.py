# TODO: module needs checking ang changing
"""
Module used to handle projects and the projects' database
"""
import base64
import json
from uuid import uuid4

import consts
from consts import DatabaseType
from data_models import Project, NewProject, ReturnedProject
from errors import DeviceNotFoundError
from db import DBHandler, DBUtils
from initialize_server import init_project_storage
from storage_handler import merge_results, zip_additional_results
from authentication import authenticate_creator


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
        IDNotFoundError

    """
    project_id = uuid4().hex
    init_project_storage(project_id)
    store_serialized_project(new_project, project_id)

    project = Project(project_id=project_id)
    if not (creator := DBUtils.find_in_db(new_project.creator_id, DatabaseType.devices_db)):
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

    results = merge_results(project_id)
    additional_results = zip_additional_results(project_id)

    returned_project = ReturnedProject(results=results, base64_zipped_additional_results=additional_results)

    return returned_project


def store_serialized_project(base64_project: NewProject, project_id: str):
    # decoded_class = base64.b64decode(base64_project.base64_serialized_class.encode('utf-8'))
    # decoded_iterable = base64.b64decode(base64_project.base64_serialized_iterable.encode('utf-8'))
    serialized_project_path = f'{consts.PROJECTS_DIRECTORY}/{project_id}' \
                              f'{consts.PROJECT_STORAGE_PROJECT}' \
                              f'{consts.PROJECT_STORAGE_JSON_PROJECT}'
    # TODO: validate base64

    project = {consts.JSON_PROJECT_BASE64_SERIALIZED_CLASS: base64_project.base64_serialized_class,
               consts.JSON_PROJECT_BASE64_SERIALIZED_ITERABLE: base64_project.base64_serialized_iterable}
    with open(serialized_project_path, 'w') as file:
        json.dump(project, file)


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


# TODO: not sure that is needed
def encode_zipped_project(project_id: str) -> bytes:
    zipped_project_path = consts.PROJECTS_DIRECTORY + '/' + project_id \
                          + consts.PROJECT_STORAGE_PROJECT \
                          + consts.PROJECT_STORAGE_JSON_PROJECT

    with open(zipped_project_path, 'rb') as file:
        zipped_project = file.read()

    encoded_project = base64.b64encode(zipped_project)

    return encoded_project
