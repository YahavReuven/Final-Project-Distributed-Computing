# TODO: module needs checking ang changing
"""
Module used to handle projects and the projects' database
"""
import os
import base64
from uuid import uuid4
from typing import Union

import asyncio

# from fastapi import File, UploadFile, Body
# from pydantic import BaseModel

import consts
from consts import DatabaseType
from data_models import Project, NewProject
from errors import IDNotFoundError
from db_handler import DBHandler, find_device
# from db_functions import find_device

from initialize_server import init_project_storage


#
# class ProjectDB(BaseModel):
#     project_id: int
#     creator_id: int
#     tasks: dict[int, int]  # dict[iteration, return value]

# ---------------------------------------------------------------------------
# send request:
# import requests
# import base64
# device1 = requests.post('http://127.0.0.1:8000/register_device')
# print(device1.text)
# device2 = requests.post('http://127.0.0.1:8000/register_device')
# b64 = base64.b64encode(b'\x54\x43\x65')
# project1 = requests.post('http://127.0.0.1:8000/upload_new_project', json={'creator_id': device1.text[1:-1],'zip_project': b64.decode('utf-8')})
# ---------------------------------------------------------------------------

# TODO: make it work with UploadFile instead of bytes
async def create_new_project(new_project: NewProject) -> str:
    """
    Create a new project, initializes its storage and updates the database.

    Args:
        new_project (NewProject): contains the needed information about
        the uploaded project.

    Returns:
        str: the project's id.

    Raises:
        IDNotFoundError

    """
    project_id = uuid4().hex
    # TODO: check if id is already in use.
    init_project_storage(project_id)
    store_zipped_project(new_project.zip_project, project_id)

    project = Project(project_id=project_id)
    if not (creator := find_device(new_project.creator_id)):
        raise IDNotFoundError()
    db = DBHandler()

    db.add_to_database(project, DatabaseType.projects_db)
    # db.projects_db[consts.PROJECTS_DATABASE_KEY].append(project)
    creator.projects.append(project)

    return project_id


async def return_project_results():
    pass


def store_zipped_project(base64_project: str, project_id: str):
    decoded_project = base64.b64decode(base64_project)
    zipped_project_path = consts.PROJECTS_DIRECTORY + '/' + project_id \
                          + consts.PROJECT_STORAGE_PROJECT \
                          + consts.PROJECT_STORAGE_ZIPPED_PROJECT_NAME_AND_TYPE

    with open(zipped_project_path, 'wb') as file:
        file.write(decoded_project)


def encode_zipped_project(project_id: str) -> bytes:
    zipped_project_path = consts.PROJECTS_DIRECTORY + '/' + project_id \
                          + consts.PROJECT_STORAGE_PROJECT \
                          + consts.PROJECT_STORAGE_ZIPPED_PROJECT_NAME_AND_TYPE

    with open(zipped_project_path, 'rb') as file:
        zipped_project = file.read()

    encoded_project = base64.b64encode(zipped_project)

    return encoded_project


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