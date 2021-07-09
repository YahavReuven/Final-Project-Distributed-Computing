import json
from typing import Union, Any
from dataclasses import asdict
from functools import wraps

from consts import Client, DEVICES_DATABASE_NAME


def singleton(cls):
    """ An implementation of singleton using decorator. """
    _instances = {}

    @wraps(cls)
    def wrapper(*args, **kwargs):
        return _instances.setdefault(cls.__name__, cls(*args, **kwargs))

    return wrapper


class ClientEncoder(json.JSONEncoder):
    """ Custom class to encode client in order to dump to json file. """

    def default(self, client: Client) -> dict[str, Union[str, list[str]], bool]:
        """ Called in case json can't serialize object. """
        return asdict(client)


class ClientDecoder(json.JSONDecoder):
    def __init__(self):
        super().__init__(object_hook=self.dict_to_client)

    @staticmethod
    def dict_to_client(obj: Any) -> Union[Client, Any]:
        """ Called for every json object. """
        if isinstance(obj, dict) and 'projects' in obj:
            return Client(**obj)
        return obj


@singleton
class DBHandler:
    """ Class to handle DB related tasks. """

    def __init__(self):
        self._load_db()

    def _load_db(self) -> None:
        with open(DEVICES_DATABASE_NAME, 'r') as file:
            self._db = json.load(file, cls=ClientDecoder)

    def update_db(self) -> None:
        print('updating db...')
        with open(DEVICES_DATABASE_NAME, 'w') as file:
            json.dump(self._db, file, cls=ClientEncoder)

    @property
    def db(self) -> dict[str, list[Client]]:
        return self._db


