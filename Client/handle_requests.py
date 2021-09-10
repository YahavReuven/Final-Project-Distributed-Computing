"""
Module used to handle sending and receiving requests, and handle the connection with the server.
"""
import requests

from handle_responses import (handle_register_response, handle_new_task_response,
                              handle_upload_task_results)
from data_models import ReturnedTask

# TODO: maybe change that the functions receive a UsersDataHandler object


def request_register_device(server_ip, server_port) -> str:
    response = requests.get(f'http://{server_ip}:{server_port}/register_device')
    return handle_register_response(response)


def request_get_new_task(server_ip, server_port, device_id) -> ReturnedTask:
    response = requests.get(f'http://{server_ip}:{server_port}/get_new_task?'
                            f'device_id={device_id}')
    return handle_new_task_response(response)


def request_upload_task_results(returned_task: ReturnedTask):
    response = requests.post('http://127.0.0.1:8000/upload_task_results',
                            json={'worker_id': returned_task.device_id, 'project_id': returned_task.project_id,
                                  'task_number': returned_task.task_number,
                                  'results': returned_task.results,
                                  'base64_zipped_additional_results': returned_task.base64_zipped_additional_results,
                                  'stop_called': returned_task.stop_called, 'is_exhausted': returned_task.is_exhausted})

    return handle_upload_task_results(response)
