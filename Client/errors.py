"""
Module used to define custom errors.
"""
from requests import Response
import json
import http


class InvalidIPv4Address(Exception):
    """ Error raised if an invalid IPv4 address is supplied. """


class InvalidPortNumber(Exception):
    """Error raised if an invalid port number is supplied. """


class ServerError(Exception):
    """An error has occurred in the server"""


def check_response_error(response: Response):
    if response.status_code != http.HTTPStatus.OK:
        handle_server_errors(response)


def handle_server_errors(response: Response):
    message = json.loads(response.text).get('message')  # TODO: make sure every error has 'message'
    print(message)
    raise ServerError
