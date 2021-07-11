import json
from typing import Union, Any
from dataclasses import asdict
from functools import wraps

from consts import Device, Project, DEVICES_DATABASE_NAME


def singleton(cls):
    """ An implementation of singleton using decorator. """
    _instances = {}

    @wraps(cls)
    def wrapper(*args, **kwargs):
        return _instances.setdefault(cls.__name__, cls(*args, **kwargs))

    return wrapper


class CustomEncoder(json.JSONEncoder):
    """ Custom class to encode client in order to dump to json file. """

    def default(self, obj: object) -> dict[str, Union[str, list[str]], bool]:
        """ Called in case json can't serialize object. """
        if isinstance(obj, Device) or isinstance(obj, Project):
            return asdict(obj)
        return json.jsonEncoder.default(self, obj)


class CustomDecoder(json.JSONDecoder):
    def __init__(self):
        super().__init__(object_hook=self.dict_to_object)

    @staticmethod
    def dict_to_object(obj: object) -> Union[Device, Any]:
        """ Called for every json object. """
        if isinstance(obj, dict) and 'projects' in obj:
            return Device(**obj)
        if isinstance(obj, dict) and 'tasks' in obj:
            return Project(**obj)
        return obj


@singleton
class DBHandler:
    """ Class to handle DB related tasks. """

    def __init__(self):
        self._load_db()

    def _load_db(self) -> None:
        with open(DEVICES_DATABASE_NAME, 'r') as file:
            self._db = json.load(file, cls=CustomDecoder)

    def update_db(self) -> None:
        print('updating db...')
        with open(DEVICES_DATABASE_NAME, 'w') as file:
            json.dump(self._db, file, cls=CustomEncoder)

    @property
    def db(self) -> dict[str, list[Device]]:
        return self._db


