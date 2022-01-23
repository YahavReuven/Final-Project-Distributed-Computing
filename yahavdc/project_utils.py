import base64

import dill


def create_class_to_send(cls):
    """

    Args:
        cls: the parallel class.

    Returns:
        str: the encoded class in str form.

    """
    serialized_class = dill.dumps(cls)
    encoded_class = base64.b64encode(serialized_class).decode('utf-8')
    return encoded_class


def create_iterable_to_send(iterable):
    serialized_iterable = dill.dumps(iterable)
    encoded_iterable = base64.b64encode(serialized_iterable).decode('utf-8')
    return encoded_iterable
