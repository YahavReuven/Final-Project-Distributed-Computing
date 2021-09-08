"""
Module used to handle and parse responses from the server.
"""
import json

from requests import Response

from data_models import Task

# TODO: add error handler


def handle_register_response(response: Response):
    return response.text[1:-1]


def handle_new_task_response(response: Response):
    content = response.text
    task_data = json.loads(content)
    return Task(**task_data)


def handle_upload_task_results(response: Response):
    return True
