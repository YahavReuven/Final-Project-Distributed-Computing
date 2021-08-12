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
FINISHED_PROJECTS_DATABASE_KEY = 'finished'


PROJECT_STORAGE_PROJECT = '/project'
PROJECT_STORAGE_RESULTS = '/results'

PROJECT_STORAGE_JSON_PROJECT = '/project.json'

JSON_PROJECT_BASE64_SERIALIZED_CLASS = 'base64_serialized_class'
JSON_PROJECT_BASE64_SERIALIZED_ITERABLE = 'base64_serialized_iterable'


SENT_TASK_VALIDITY = timedelta(days=1)
SENT_TASK_DATE_KEY = 'sent_date'
DATETIME_FORMAT_IN_DB = '%d-%m-%Y %H:%M:%S'


RETURNED_TASK_TEMP_ZIPPED_RESULTS_FILE = '/temp.zip'
RETURNED_TASK_RESULTS_DIRECTORY = '/results'


UPDATE_DB_DELAY = 60*0.1


class DatabaseType(str, Enum):
    devices_db = 'devices_db'
    projects_db = 'projects_db'
    finished_projects_db = 'finished_db'


class ProjectsDatabaseType(str, Enum):
    projects_db = 'projects_db'
    finished_projects_db = 'finished_db'
    both = 'both'






