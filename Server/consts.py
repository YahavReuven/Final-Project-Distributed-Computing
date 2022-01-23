"""
Module used to define constants.
"""
from datetime import timedelta
from enum import Flag, auto

PORT = 8000

DEVICES_DIRECTORY = 'devices'
DEVICES_DATABASE_NAME = 'devices_database.json'

PROJECTS_DIRECTORY = 'projects'
PROJECTS_DATABASE_NAME = 'projects_database.json'
PROJECT_STORAGE_PROJECT = 'project'
PROJECT_STORAGE_RESULTS = 'results'
PROJECT_STORAGE_JSON_PROJECT = 'project.json'

RETURNED_TASK_TEMP_ZIPPED_RESULTS_FILE = 'temp_results.zip'
RETURNED_TASK_RESULTS_DIRECTORY = 'results'
RETURNED_TASK_ADDITIONAL_RESULTS_DIRECTORY = 'additional_results'
TEMP_PROJECT_ADDITIONAL_RESULTS_DIRECTORY = 'temp'
RESULTS_FILE = 'results.json'

SENT_TASK_VALIDITY = timedelta(days=1)
DATETIME_FORMAT = '%d-%m-%Y %H:%M:%S'

UPDATE_DB_DELAY = 60*0.1


class DatabaseType(Flag):
    devices_db = auto()
    active_projects_db = auto()
    finished_projects_db = auto()
    waiting_to_return_projects_db = auto()
    projects_db = (active_projects_db | finished_projects_db |
                   waiting_to_return_projects_db)
