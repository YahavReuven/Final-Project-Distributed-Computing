"""
Module used for json custom handling.
"""
import json

from data_models import User


class CustomDecoder(json.JSONDecoder):
    def __init__(self):
        super().__init__(object_hook=self.dict_to_object)

    @staticmethod
    def dict_to_object(obj: object):
        """Called for every json object."""
        if isinstance(obj, dict) and 'ip' in obj:
            return User(**obj)
        return obj
.