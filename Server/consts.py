"""
Module used to define constants.
"""

from datetime import timedelta
from enum import Enum
import data_models

DEVICES_DATABASE_DIRECTORY = './devices'
DEVICES_DATABASE_NAME = DEVICES_DATABASE_DIRECTORY + '/devices_database.json'
DEVICES_DATABASE_KEY = 'devices'

PROJECTS_DIRECTORY = './projects'
PROJECTS_DATABASE_NAME = PROJECTS_DIRECTORY + '/projects_database.json'
PROJECTS_DATABASE_KEY = 'projects'

PROJECT_STORAGE_PROJECT = '/project'
PROJECT_STORAGE_RESULTS = '/results'

PROJECT_STORAGE_ZIPPED_PROJECT_NAME_AND_TYPE = '/zipped_project.zip'

SENT_TASK_VALIDITY = timedelta(days=1)
SENT_TASK_DATE_KEY = 'sent_date'
DATETIME_FORMAT_IN_DB = '%d-%m-%Y %H:%M:%S'

UPDATE_DB_DELAY = 60*0.1


class DatabaseType(str, Enum):
    devices_db = 'devices_db'
    projects_db = 'projects_db'






