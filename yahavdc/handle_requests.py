"""
Module used to handle requests sent to the server.
"""
import requests

from data_models import NewProject
from handle_responses import handle_new_project_response, handle_get_project_response


def request_upload_new_project(server_ip: str, server_port: str, project: NewProject):
    """
    Sends a request to create a new project.

    Args:
        server_ip (str): the server's ip.
        server_port (str): the server's port.
        project (NewProject): the project to be sent.

    Returns:
        str: the project's id.

    """
    response = requests.post(
        f'http://{server_ip}:{server_port}/upload_new_project',
        json={'creator_id': project.creator_id,
              'task_size': project.task_size,
              'parallel_func': project.parallel_func,
              'stop_func': project.stop_func,
              'only_if_func': project.only_if_func,
              'base64_serialized_class': project.base64_serialized_class,
              'base64_serialized_iterable': project.base64_serialized_iterable,
              'modules': project.modules})

    return handle_new_project_response(response)


def request_get_project_results(server_ip: str, server_port: str, device_id: str,
                                project_id: str):
    """
    Sends a request to get the results of a project.

    Args:
        server_ip (str): the server's ip.
        server_port (str): the server's port.
        device_id (str): the id of the creator of the project.
        project_id (str): the id of the project.

    Returns:
        ReturnedProject: the results and statistics of the project.

    """
    response = requests.get(f'http://{server_ip}:{server_port}/get_project_results?'
                            f'device_id={device_id}&project_id={project_id}')

    return handle_get_project_response(response)
.