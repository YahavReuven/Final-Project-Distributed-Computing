"""
Module used to handle sending and receiving requests, and handle the connection with the server.
"""
import requests

from handle_responses import handle_register_response, handle_new_task_response
from handle_users_data import UsersDataHandler

# TODO: check for errors
# TODO: maybe change that the functions receive a UsersDataHandler object


def request_register_device(user: UsersDataHandler) -> str:
    server_ip = user.ip
    server_port = user.port
    response = requests.get(f'http://{server_ip}:{server_port}/register_device')
    return handle_register_response(response)


def request_get_new_task(user: UsersDataHandler):
    server_ip = user.ip
    server_port = user.port
    device_id = user.device_id
    response = requests.get(f'http://{server_ip}:{server_port}/get_new_task?'
                            f'device_id={device_id}')
    return handle_new_task_response(response)
