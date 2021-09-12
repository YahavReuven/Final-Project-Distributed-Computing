"""
Module used to define constants.
"""
from enum import Enum

USERS_DIRECTORY = 'users'

TASKS_DIRECTORY = 'task'
RESULTS_FILE = 'results'
ADDITIONAL_RESULTS_DIRECTORY = 'additional_results'
ADDITIONAL_RESULTS_ZIP_FILE = 'additional_results'

JSON_EXTENSION = '.json'

PARALLEL_FUNCTION_NAME = 'parallel_func'
STOP_FUNCTION_NAME = 'stop_func'


MIN_PORT_NUM = 1
MAX_PORT_NUM = 65535


class ReturnTypes(str, Enum):
    normal = 'normal'
    exhausted = 'exhausted'
    stopped = 'stopped'
