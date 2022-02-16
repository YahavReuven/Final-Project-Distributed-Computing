"""
Module used to provide utils for a project
"""
import base64
from typing import Iterator

import dill


def create_class_to_send(cls):
    """
    Encodes the parallel class in order to send it to the server.

    Args:
        cls: the parallel class.

    Returns:
        str: the encoded representation of the class.

    """
    serialized_class = dill.dumps(cls)
    encoded_class = base64.b64encode(serialized_class).decode('utf-8')
    return encoded_class


def create_iterator_to_send(iterator: Iterator):
    """
    Encodes the iterator in order to send it to the server.

    Args:
        iterator (Iterator): the iterator to be encoded.

    Returns:
        str: the encoded representation of the iterator.

    """
    serialized_iterable = dill.dumps(iterator)
    encoded_iterable = base64.b64encode(serialized_iterable).decode('utf-8')
    return encoded_iterable
