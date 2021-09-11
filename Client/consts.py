"""
Module used to define constants.
"""
from enum import Enum

USERS_DIRECTORY = 'users'

USER_IP_KEY = 'ip'
USER_PORT_KEY = 'port'
USER_DEVICE_ID_KEY = 'device_id'
USER_PROJECTS_KEY = 'projects'
USER_TASKS_KEY = 'tasks'

TASKS_DIRECTORY = 'task'
RESULTS_FILE = 'results'
ADDITIONAL_RESULTS_DIRECTORY = 'additional_results'
ADDITIONAL_RESULTS_ZIP_FILE = 'additional_results'

JSON_EXTENSION = '.json'

PARALLEL_FUNCTION_NAME = 'parallel_func'
STOP_FUNCTION_NAME = 'stop_func'


# TODO: find a better way
RETURNED_TASK_WORKER_ID_KEY = 'worker_id'
RETURNED_TASK_PROJECT_ID_KEY = 'project_id'
RETURNED_TASK_TASK_NUMBER_KEY = 'task_number'
RETURNED_TASK_RESULTS_KEY = 'results'
RETURNED_TASK_BASE64_ZIPPED_ADDITIONAL_RESULTS_KEY = 'base64_zipped_additional_results'
RETURNED_TASK_STOP_CALLED_KEY = 'stop_called'
RETURNED_TASK_IS_EXHAUSTED_KEY = 'is_exhausted'


MIN_PORT_NUM = 1
MAX_PORT_NUM = 65535


class ReturnTypes(str, Enum):
    normal = 'normal'
    exhausted = 'exhausted'
    stopped = 'stopped'
