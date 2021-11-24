"""
Module used to handle conversion between json and object.
"""
import json
from dataclasses import asdict
from datetime import timedelta

from data_models import User, StorageTaskStatistics, TaskStatistics


class CustomEncoder(json.JSONEncoder):
    """ Custom class to encode client in order to dump to json file. """

    def default(self, obj: object):  # -> dict[str, Union[str, list[str]], bool]:
        """ Called in case json can't serialize object. """
        if isinstance(obj, User):
            return asdict(obj)
        if isinstance(obj, StorageTaskStatistics):
            return asdict(obj)
        if isinstance(obj, TaskStatistics):
            return asdict(obj)
        if isinstance(obj, timedelta):
            return str(obj)
        return super().default(obj)


class CustomDecoder(json.JSONDecoder):
    def __init__(self):
        super().__init__(object_hook=self.dict_to_object)

    @staticmethod
    def dict_to_object(obj: object):
        """ Called for every json object. """
        if isinstance(obj, dict) and 'ip' in obj:
            return User(**obj)
        if isinstance(obj, dict) and 'task_number' in obj:
            return StorageTaskStatistics(**obj)
        if isinstance(obj, dict) and 'pure_run_time' in obj:
            return TaskStatistics(**obj)
        return obj
