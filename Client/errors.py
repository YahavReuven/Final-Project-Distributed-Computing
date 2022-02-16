"""
Module used to define custom errors.
"""
import json
import http

from requests import Response


class InvalidIPv4Address(Exception):
    """Error raised if an invalid IPv4 address is supplied."""


class InvalidPortNumber(Exception):
    """Error raised if an invalid port number is supplied."""


class ServerError(Exception):
    """An error has occurred in the server."""


def check_response_error(response: Response):
    """
    Checks if an OK response was returned and handles it if not.

    Args:
        response (Response): the response's representation.

    """
    if response.status_code != http.HTTPStatus.OK:
        handle_server_errors(response)


def handle_server_errors(response: Response):
    """
    Prints the error message given in a non-OK response.

    Args:
        response (Response): the response's representation.

    Raises:
        ServerError: always raises this error.

    """
    message = json.loads(response.text).get('message')
    print(message)
    raise ServerError
