from http import HTTPStatus

from fastapi import Request
from fastapi.responses import JSONResponse


class ServerError(Exception):
    """Error raised for a general error in the server"""
    message = 'internal server error'
    status_code = HTTPStatus.INTERNAL_SERVER_ERROR


class BadRequestError(ServerError):
    """Error raised when a bad request is received"""
    message = 'bad request'
    status_code = HTTPStatus.BAD_REQUEST


class IDNotFoundError(BadRequestError):
    """Error raised if the received ID is invalid or is not present in the database."""
    message = 'id not found'


async def handle_server_error(request: Request, exc: ServerError) -> JSONResponse:

    return JSONResponse(status_code=exc.status_code,
                        content={'message': exc.message})

