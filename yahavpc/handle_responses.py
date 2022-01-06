import json

from requests import Response

from data_models import ReturnedProject
from errors import check_response_error

# TODO: add error checking


def handle_new_project_response(response: Response):
    return response.text[1:-1]


def handle_get_project_response(response: Response):
    content = response.text
    project_data = json.loads(content)
    check_response_error(response)
    return ReturnedProject(**project_data)
