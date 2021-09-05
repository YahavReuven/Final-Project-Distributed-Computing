"""
Module used for the authentication of id's sent to the server from the client.
"""

from typing import Union

from db import DBUtils
from consts import DatabaseType
from data_models import Worker, Task
from errors import DeviceNotFoundError, ProjectNotFoundError, WorkerNotAuthenticatedError


# TODO: check docstring
def authenticate_device(device_id: str):
    """
    Checks if a device with the given device_id is present in the database.

    Args:
        device_id (str): the device id of the desired device.

    Raises:
        DeviceNotFoundError: if a device with the given device_id is not
        present in the database.
    """

    device = DBUtils.find_in_db(device_id, DatabaseType.devices_db)
    if not device:
        raise DeviceNotFoundError


def authenticate_creator(device_id: str, project_id: str) -> bool:

    authenticate_device(device_id)

    device = DBUtils.find_in_db(device_id, DatabaseType.devices_db)

    for project in device.projects:
        if project.project_id == project_id:
            return True

    raise ProjectNotFoundError


def authenticate_project(project_id: str) -> bool:

    project = DBUtils.find_in_db(project_id, DatabaseType.projects_db)

    if not project:
        raise ProjectNotFoundError

    return True


def authenticate_worker(worker_id: str, task: Task) -> Union[Worker, None]:
    for worker in task.workers:
        if worker.worker_id == worker_id:
            return worker

    raise WorkerNotAuthenticatedError
