"""
Module used to define costume errors.
"""
import json
import http

from requests import Response


class FunctionNotFoundError(Exception):
    """A function is not present in the given class."""


class ParallelFunctionNotFoundError(FunctionNotFoundError):
    """A parallel function is not present in the given class."""


class UnsupportedSpecialFunctionsCombination(Exception):
    """An unsupported combination of special functions was used."""


class UserNotFoundError(Exception):
    """The user was not found."""


class ResultsBeforeCreationError(Exception):
    """
    Error raised if a get_results method of a project was called
    before the project was initialized.
    """


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
