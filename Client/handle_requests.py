"""
Module used to handle sending and receiving requests, and handle the connection with the server.
"""
import requests

from handle_responses import handle_register_response, handle_new_task_response, handle_upload_task_results
#from TOCHECK_handle_users_data import UsersDataHandler

# TODO: check for errors
# TODO: maybe change that the functions receive a UsersDataHandler object


def request_register_device(server_ip, server_port) -> str:
    # server_ip = user.ip
    # server_port = user.port
    response = requests.get(f'http://{server_ip}:{server_port}/register_device')
    return handle_register_response(response)


def request_get_new_task(server_ip, server_port, device_id):
    # server_ip = user.ip
    # server_port = user.port
    # device_id = user.device_id
    response = requests.get(f'http://{server_ip}:{server_port}/get_new_task?'
                            f'device_id={device_id}')
    return handle_new_task_response(response)


def request_upload_task_results(device_id, project_id, task_number, results,
                        base64_zipped_additional_results = None, stop_called = False,
                        is_exhausted = False):
    response = requests.post('http://127.0.0.1:8000/upload_task_results',
                            json={'worker_id': device_id, 'project_id': project_id,
                                  'task_number': task_number,
                                  'results': results,
                                  'base64_zipped_additional_results': base64_zipped_additional_results,
                                  'stop_called': stop_called, 'is_exhausted': is_exhausted})

    return handle_upload_task_results(response)
