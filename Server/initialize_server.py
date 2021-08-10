"""
Module used to initialize the server and update the database in file
"""

import time
import os

import consts
from db_handler import DBHandler


def update_db(db: DBHandler):
    """
    Updates the server to a file every consts.UPDATE_DB_DELAY time
    """
    while True:
        time.sleep(consts.UPDATE_DB_DELAY)
        db.update_db()


def init_server():
    """
    Initializes the servers database files
    """
    init_devices_database()
    init_projects_database()


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
            database.write('{ "' + consts.PROJECTS_DATABASE_KEY + '" : [] , "'
                           + consts.FINISHED_PROJECTS_DATABASE_KEY + '" : [] }')


def init_project_storage(project_id: str):
    """

    Initializes the project with the project's id storage space.

    Note:
        Assumes that the project's id appears once in the database.

    Args:
        project_id (str): the project's id

    """

    project_directory = f'{consts.PROJECTS_DIRECTORY}/{project_id}'

    # TODO: shouldn't return False since ids are unique. maybe check.
    os.makedirs(f'{project_directory}{consts.PROJECT_STORAGE_PROJECT}')
    os.makedirs(f'{project_directory}{consts.PROJECT_STORAGE_RESULTS}')
