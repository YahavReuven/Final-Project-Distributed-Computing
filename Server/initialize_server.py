"""
Module used to initialize the server and update the backup database files.
"""
import json
import time
import os

import consts
from db import DBHandler, CustomEncoder
from utils import create_path_string
from data_models import DevicesDB, ProjectsDB


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
    #db.init_device_dbs_to_devices()


def init_devices_database():
    """
    Initializes the devices' database backup file and creates the needed directories.
    """
    devices_path = create_path_string(consts.DEVICES_DIRECTORY)
    os.makedirs(devices_path, exist_ok=True)

    devices_database_file = create_path_string(devices_path,
                                               consts.DEVICES_DATABASE_NAME,
                                               from_current_directory=False)
    if not os.path.isfile(devices_database_file):
        #template = {consts.DEVICES_DATABASE_KEY: []}
        with open(devices_database_file, 'w') as file:
            json.dump(DevicesDB(), file, cls=CustomEncoder)


def init_projects_database():
    """
    Initializes the projects' database backup files and creates the needed directories.
    """
    projects_path = create_path_string(consts.PROJECTS_DIRECTORY)
    os.makedirs(projects_path, exist_ok=True)

    projects_database_file = create_path_string(projects_path,
                                                consts.PROJECTS_DATABASE_NAME,
                                                from_current_directory=False)
    if not os.path.isfile(projects_database_file):
        # template = {consts.ACTIVE_PROJECTS_DB_KEY: [],
        #             consts.WAITING_TO_RETURN_PROJECTS_DB_KEY: [],
        #             consts.FINISHED_PROJECTS_DB_KEY: []
        #             }
        with open(projects_database_file, 'w') as file:
            json.dump(ProjectsDB(), file, cls=CustomEncoder)


# TODO: move to storage_handler
def init_project_storage(project_id: str):
    """
    Initializes the project with the project's id storage space.
    """
    project_directory = create_path_string(consts.PROJECTS_DIRECTORY, project_id)

    os.makedirs(create_path_string(project_directory, consts.PROJECT_STORAGE_PROJECT,
                                   from_current_directory=False))
    os.makedirs(create_path_string(project_directory, consts.PROJECT_STORAGE_RESULTS,
                                   from_current_directory=False))
