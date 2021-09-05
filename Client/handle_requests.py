"""
Module used to handle sending and receiving requests, and handle the connection with the server.
"""
import requests

# TODO: check for errors
# TODO: change parsing
def register_device(server_ip, server_port) -> str:
    response = requests.get(f'http://{server_ip}:{server_port}/register_device')
    return response.text[1:-1]