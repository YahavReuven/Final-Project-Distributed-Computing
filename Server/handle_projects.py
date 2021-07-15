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
from pydantic import BaseModel

import consts
from consts import Project

from db_handler import DBHandler, find_device
# from db_functions import find_device

from initialize_server import init_project_storage


# db = None
#
# def projects_db_init():
#     global db
#     db = DBHandler()

# def new_project_1():
#     db = DBHandler()
#     project_id = uuid4().hex
#     project = consts.Project(project_id=project_id)
#     db.projects_db[consts.PROJECTS_DATABASE_KEY].append(project)
#     return project_id


class NewProject(BaseModel):
    creator_id: str  # TODO: the device id of the creator of the project. maybe change to user
    zip_project: str  # in base 64 encoding


#
# class ProjectDB(BaseModel):
#     project_id: int
#     creator_id: int
#     tasks: dict[int, int]  # dict[iteration, return value]

# send request:
# import base64
# b64 = base64.b64encode(b'\x54\x43\x65')
# resp = requests.post('http://127.0.0.1:8000/new_project', json={'creator_id': 1,'zip_project': b64.decode('utf-8')})


# TODO: make it work with UploadFile instead of bytes
async def create_new_project(new_project: NewProject) -> str:
    """
    Create a new project, initializes its storage and updates the database.

    Args:
        new_project (NewProject): contains the needed information about
        the uploaded project.

    Returns:
        str: the project's id.

    """
    project_id = uuid4().hex
    # TODO: check if id is already in use.
    init_project_storage(project_id)
    store_zipped_project(new_project.zip_project, project_id)

    project = Project(project_id=project_id)
    creator = find_device(new_project.creator_id)
    db = DBHandler()

    db.projects_db[consts.PROJECTS_DATABASE_KEY].append(project)
    creator.projects.append(project)

    return project_id


#
#
# async def return_project_results():
#     pass
#
#
#

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