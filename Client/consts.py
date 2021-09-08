
from enum import Enum

USERS_DIRECTORY = 'users'
# DATA_FILE = 'data.json'

DATA_IP_KEY = 'ip'
DATA_PORT_KEY = 'port'
DATA_DEVICE_ID_KEY = 'device_id'
DATA_PROJECTS_KEY = 'projects'
DATA_TASKS_KEY = 'tasks'

TASKS_DIRECTORY = 'task'
RESULTS_FILE = 'results'
ADDITIONAL_RESULTS_DIRECTORY = 'additional_results'
ADDITIONAL_RESULTS_ZIP_FILE = 'additional_results'


PARALLEL_FUNCTION_NAME = 'parallel_func'
STOP_FUNCTION_NAME = 'stop_func'

JSON_EXTENSION = '.json'




MIN_PORT_NUM = 1
MAX_PORT_NUM = 65535


class ReturnTypes(Enum):
    normal = 'normal'
    exhausted = 'exhausted'
    stopped = 'stopped'
