import requests

from data_models import NewProject
from handle_responses import handle_new_project_response, handle_get_project_response


def request_upload_new_project(server_ip: str, server_port, project: NewProject):
    response = requests.post(f'http://{server_ip}:{server_port}/upload_new_project',
                             json={'creator_id': project.creator_id,
                                   'task_size': project.task_size,
                                   'base64_serialized_class': project.base64_serialized_class,
                                   'base64_serialized_iterable': project.base64_serialized_iterable})

    return handle_new_project_response(response)


def request_get_project_results(server_ip: str, server_port, device_id: str, project_id: str):
    response = requests.get(f'http://{server_ip}:{server_port}/get_project_results?'
                            f'device_id={device_id}&project_id={project_id}')

    return handle_get_project_response(response)
