from enum import Enum

RESULTS_NAME_AND_TYPE = '/results.csv'
RESULTS_HEADERS = ['ITERATION', 'RETURN_VALUE_OR_ERROR']


class Returns(Enum):
    normal = 'normal'
    exhausted = 'exhausted'
    stopped = 'stopped'


