
import json
from dataclasses import asdict

from data_models import User

class CustomEncoder(json.JSONEncoder):
    """ Custom class to encode client in order to dump to json file. """

    def default(self, obj: object):  # -> dict[str, Union[str, list[str]], bool]:
        """ Called in case json can't serialize object. """
        if isinstance(obj, User):
            return asdict(User)
        return super().default(obj)


class CustomDecoder(json.JSONDecoder):
    def __init__(self):
        super().__init__(object_hook=self.dict_to_object)

    @staticmethod
    def dict_to_object(obj: object):
        """ Called for every json object. """
        if isinstance(obj, dict) and 'ip' in obj:
            return User(**obj)
        return obj