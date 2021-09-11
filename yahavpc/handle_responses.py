import json

from requests import Response

from data_models import ReturnedProject

# TODO: add error checking


def handle_new_project_response(response: Response):
    return response.text[1:-1]


def handle_get_project_response(response: Response):
    content = response.text
    project_data = json.loads(content)
    return ReturnedProject(**project_data)
