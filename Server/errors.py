from http import HTTPStatus

from fastapi import Request
from fastapi.responses import JSONResponse


class IDNotFoundError(Exception):
    """Error raised if the received ID is invalid or is not present in the database."""


async def handle_id_not_found_error(request: Request, exc: IDNotFoundError) -> JSONResponse:

    return JSONResponse(status_code=HTTPStatus.BAD_REQUEST,
                        content={'message': 'Id not found.'})
