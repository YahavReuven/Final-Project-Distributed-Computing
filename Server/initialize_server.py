"""
Module used to initialize the server and update
"""

import time
import os

import consts
from db_handler import DBHandler


def update_db(db: DBHandler):
    while True:
        time.sleep(consts.UPDATE_DB_DELAY)
        db.update_db()


def init_server():
    init_devices_database()
    init_projects_database()
    # db = DBHandler()  # TODO: not sure if needed


def init_devices_database():
    """
    Initializes devices database and creates needed directories.
    """

    os.makedirs(consts.DEVICES_DATABASE_DIRECTORY, exist_ok=True)

    if not os.path.isfile(consts.DEVICES_DATABASE_NAME):
        with open(consts.DEVICES_DATABASE_NAME, 'w') as database:
            database.write('{ "' + consts.DEVICES_DATABASE_KEY + '" : [] }')


def init_projects_database():
    """
    Initializes projects database and creates needed directories.
    """

    os.makedirs(consts.PROJECTS_DIRECTORY, exist_ok=True)

    if not os.path.isfile(consts.PROJECTS_DATABASE_NAME):
        with open(consts.PROJECTS_DATABASE_NAME, 'w') as database:
            database.write('{ "' + consts.PROJECTS_DATABASE_KEY + '" : [] }')


def init_project_storage(project_id: str):
    """

    Initializes the project with the project's id storage space.

    Note:
        Assumes that the project's id appears once in the database.

    Args:
        project_id (str): the project's id

    """

    project_directory = consts.PROJECTS_DIRECTORY + '/' + project_id

    # TODO: shouldn't return False since ids are unique. maybe check.
    os.makedirs(project_directory + consts.PROJECT_STORAGE_PROJECT)
    os.makedirs(project_directory + consts.PROJECT_STORAGE_RESULTS)
