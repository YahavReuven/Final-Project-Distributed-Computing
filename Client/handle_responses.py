"""
Module used to handle and parse responses from the server.
"""
import json

from requests import Response

from data_models import ReceivedTask
from errors import check_response_error

# TODO: check for errors


def handle_register_response(response: Response) -> str:
    """
    Handles the response of a register_device request to the server.

    Args:
        response (Response): the response from the server.

    Returns:
        str: the device_id of the new device.

    """
    return response.text[1:-1]


def handle_new_task_response(response: Response) -> ReceivedTask:
    """
    Handles the response of a get_new_task request to the server.

    Args:
        response (Response): the response from the server.

    Returns:
        ReceivedTask: te task received from the server.

    """
    content = response.text
    task_data = json.loads(content)
    check_response_error(response)
    return ReceivedTask(**task_data)


def handle_upload_task_results(response: Response):
    return response
