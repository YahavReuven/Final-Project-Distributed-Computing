"""
Module used to initialize the server and update the backup database files.
"""
import json
import time
import os

import consts
from db import DBHandler
from utils import create_path_string


def update_db(db: DBHandler):
    """
    Updates the server to a backup file every consts.UPDATE_DB_DELAY time.
    """
    while True:
        time.sleep(consts.UPDATE_DB_DELAY)
        db.update_db()


def init_server():
    """
    Initializes the server's database backup files.
    """
    init_devices_database()
    init_projects_database()
    db = DBHandler()
    db.init_device_dbs_to_devices()


def init_devices_database():
    """
    Initializes the devices' database backup files and creates the needed directories.
    """
    os.makedirs(create_path_string(consts.DEVICES_DIRECTORY), exist_ok=True)

    devices_database_file = create_path_string(consts.DEVICES_DIRECTORY,
                                               consts.DEVICES_DATABASE_NAME)
    if not os.path.isfile(devices_database_file):
        template = {consts.DEVICES_DATABASE_KEY: []}
        with open(devices_database_file, 'w') as file:
            json.dump(template, file)


def init_projects_database():
    """
    Initializes the projects' database backup files and creates the needed directories.
    """
    os.makedirs(create_path_string(consts.PROJECTS_DIRECTORY), exist_ok=True)

    projects_database_file = create_path_string(consts.PROJECTS_DIRECTORY,
                                                consts.PROJECTS_DATABASE_NAME)
    if not os.path.isfile(projects_database_file):
        template = {consts.ACTIVE_PROJECTS_DB_KEY: [],
                    consts.WAITING_TO_RETURN_PROJECTS_DB_KEY: [],
                    consts.FINISHED_PROJECTS_DB_KEY: []
                    }
        with open(projects_database_file, 'w') as file:
            json.dump(template, file)


# TODO: move to storage_handler
def init_project_storage(project_id: str):
    """
    Initializes the project with the project's id storage space.

    Note:
        Assumes that the project's id appears once in the database.

    Args:
        project_id (str): the project's id.
    """

    project_directory = create_path_string(consts.PROJECTS_DIRECTORY, project_id)

    os.makedirs(create_path_string(project_directory, consts.PROJECT_STORAGE_PROJECT,
                                   from_current_directory=False))
    os.makedirs(create_path_string(project_directory, consts.PROJECT_STORAGE_RESULTS,
                                   from_current_directory=False))
