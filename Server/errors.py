"""
Module used for custom errors and error handling.
"""
from http import HTTPStatus

from fastapi import Request
from fastapi.responses import JSONResponse


class ServerError(Exception):
    """Error raised for a general error in the server."""
    message = 'internal server error'
    status_code = HTTPStatus.INTERNAL_SERVER_ERROR


class BadRequestError(ServerError):
    """Error raised when a bad request is received."""
    message = 'bad request'
    status_code = HTTPStatus.BAD_REQUEST


class IDNotFoundError(BadRequestError):
    """Error raised if the received ID is not present in the database."""
    message = 'id not found'


class DeviceNotFoundError(IDNotFoundError):
    """Error raised if the received device id is not present in devices database."""
    message = 'device not found'


class ProjectNotFoundError(IDNotFoundError):
    """Error raised if the received project id is not present in projects database."""
    message = 'project not found'


class ProjectFinishedError(ProjectNotFoundError):
    """Error raised if an illegal operation was done on a finished project."""
    message = 'project is finished'


class ProjectIsActive(ProjectNotFoundError):
    """Error raised if an illegal operation was done on an active project."""
    message = 'project is active'


class UnnecessaryTaskError(ProjectFinishedError):
    """Error raised if a client tries to upload a task which is no longer needed
    (mainly due to a stop number being set)"""
    message = 'task is no longer needed'


class NoTaskAvailable(BadRequestError):
    """Error raised if there isn't a task available to send to the worker."""
    message = 'no task available'


class IDAuthenticationError(BadRequestError):
    """Error raised if a given id is not authenticated to do the action which caused
     the error to be raised"""
    message = 'id is not authenticated'


class WorkerNotAuthenticatedError(IDAuthenticationError):
    """Error raised if a worker is not authenticated to upload results to the task"""
    message = 'worker is not authenticated'


class InvalidBase64Error(BadRequestError):
    """Error raised if an invalid base64 string is received from the client."""
    message = 'invalid base64 string'


class DeviceIsBlocked(IDAuthenticationError):
    """Error raised if a blocked device tried to get a task to run."""
    message = 'blocked device'


async def handle_server_error(request: Request, exc: ServerError) -> JSONResponse:
    """
    Returns an error response to a client if one is raised.

    """
    return JSONResponse(status_code=exc.status_code,
                        content={'message': exc.message})
