"""
Module used to handle the responses given from the server.
"""
import json

from requests import Response

from data_models import ReturnedProject
from errors import check_response_error


def handle_new_project_response(response: Response) -> str:
    """
    Parses the response created from creating a new project.

    Args:
        response (Response): the response from the server.

    Returns:
        str: the project's id.

    """
    check_response_error(response)
    return response.text[1:-1]


def handle_get_project_response(response: Response) -> ReturnedProject:
    """
    Parses the response created from requesting the project's results.

    Args:
        response (Response): the response from the server.

    Returns:
        ReturnedProject: the results and statistics returned from the server.

    """
    content = response.text
    project_data = json.loads(content)
    check_response_error(response)
    return ReturnedProject(**project_data)
