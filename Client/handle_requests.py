"""
Module used to handle sending and receiving requests, and handle the
connection with the server.
"""
import requests

from handle_responses import (handle_register_response, handle_new_task_response,
                              handle_upload_task_results)
from data_models import ReturnedTask, ReceivedTask

# TODO: maybe change that the functions receives a UsersDataHandler object


def request_register_device(server_ip, server_port) -> str:
    """
    Sends a register_device request to the server.

    Args:
        server_ip: the ip of the server.
        server_port: the port on the server to send the request to.

    Returns:
        str: the device_id of the new device.

    """
    response = requests.get(f'http://{server_ip}:{server_port}/register_device')
    return handle_register_response(response)


def request_get_new_task(server_ip, server_port, device_id) -> ReceivedTask:
    """
    Sends a get_new_task request to the server.

    Args:
        server_ip: the ip of the server.
        server_port: the port on the server to send the request to.
        device_id: the device_id of the worker.

    Returns:
        ReceivedTask: te task received from the server.

    """
    response = requests.get(f'http://{server_ip}:{server_port}/get_new_task?'
                            f'device_id={device_id}')
    return handle_new_task_response(response)


def request_upload_task_results(server_ip, server_port, returned_task: ReturnedTask):
    """
    Sends an upload_task_results request to the server.

    Args:
        server_ip: the ip of the server.
        server_port: the port on the server to send the request to.
        returned_task (ReturnedTask): the task results, including additional information.

    Returns:
        ???????????
    """
    response = requests.post(f'http://{server_ip}:{server_port}/upload_task_results',
                            json={'worker_id': returned_task.worker_id,
                                  'project_id': returned_task.project_id,
                                  'task_number': returned_task.task_number,
                                  'results': returned_task.results,
                                  'base64_zipped_additional_results':
                                      returned_task.base64_zipped_additional_results,
                                  'stop_called': returned_task.stop_called,
                                  'is_exhausted': returned_task.is_exhausted})

    return handle_upload_task_results(response)
