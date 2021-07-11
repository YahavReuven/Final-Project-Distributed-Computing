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

from db_handler import DBHandler


# db = None
#
# def projects_db_init():
#     global db
#     db = DBHandler()

def new_project():
    db = DBHandler()
    project_id = uuid4().hex
    project = consts.Project(project_id=project_id)
    db.projects_db[consts.PROJECTS_DATABASE_KEY].append(project)
    return project_id




# class ProjectInfo(BaseModel):
#     creator_id: int  #TODO: the device id of the creator of the project. maybe change to user
#     zip_project: str  # in base 64 encoding
#     #zip_project: UploadFile
#
#
# class ProjectDB(BaseModel):
#     project_id: int
#     creator_id: int
#     tasks: dict[int, int]  # dict[iteration, return value]

# send request:
# import base64
# b64 = base64.b64encode(b'\x54\x43\x65')
# resp = requests.post('http://127.0.0.1:8000/new_project', json={'creator_id': 1,'zip_project': b64.decode('utf-8')})


# # TODO: make it work with UploadFile insted of bytes
# async def create_new_project(new_project: ProjectInfo) -> int:
#
#     project_id = uuid4().hex
#
#     init_project_storage(project_id)
#     store_zipped_project(new_project.zip_project, project_id)
#
#     print(new_project.creator_id, new_project.zip_project)
#     return new_project.creator_id
#
#
# # async def create_new_project(creator_id: int = Body(), somthing: int = Body()) -> int:
# #     print(creator_id)
# #     return somthing
#
# # async def create_new_project(new_project: ProjectInfo) -> int:
# #     print(new_project.creator_id)
# #     return new_project.creator_id
#
# # async def create_new_project(new_project: ProjectInfo, file: UploadFile = File(...)):
# #     #print(new_project.dict())
# #     return True
#
#
#
# async def return_project_results():
#     pass
#
#
#
# def init_projects_database():
#     """
#     Creates the directories and files needed for the project handling.
#     """
#     if not os.path.isdir(consts.PROJECTS_DATABASE_DIRECTORY):  # creates the database directory if one is not present
#         os.mkdir(consts.PROJECTS_DATABASE_DIRECTORY)
#     if not os.path.isfile(consts.PROJECTS_DATABASE_NAME):  # creates an empty database if a database is not present
#         with open(consts.PROJECTS_DATABASE_NAME, 'w') as database:
#             database.write('{}')
#
#
# # TODO: change to consts
# def store_zipped_project(raw_project: ProjectInfo.zip_project, project_id: hex) -> bool:
#
#     decoded_project = base64.b64decode(raw_project)
#     project_directory = consts.PROJECTS_DATABASE_DIRECTORY + '//' + project_id + '/project'
#
#     with open(project_directory + '/zipped_project.zip', 'wb') as file:
#         file.write(decoded_project)
#
#
# # TODO: change to consts
# def init_project_storage(project_id: hex):
#     """
#     Creates the project storage directory
#     """
#
#     project_directory = consts.PROJECTS_DATABASE_DIRECTORY + '//' + project_id
#     try:
#         os.mkdir(project_directory)
#     except FileExistsError:
#         print("project id is already in use")  # TODO: change to raise error. create new project id
#
#     os.mkdir(project_directory + './project')
#     os.mkdir(project_directory + './results')
