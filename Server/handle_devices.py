"""
Module used to handle devices.
"""
from uuid import uuid4

from consts import DatabaseType
from data_models import Device
from db import DBHandler


async def register_device() -> str:
    """
    Creates a new device and adds it to the database.

    Note:
        Assumes that './devices/devices_database.json' exists and contains
        a json object.

    Returns:
        str: the new device's id.

    """
    db = DBHandler()

    device_id = uuid4().hex
    device = Device(device_id=device_id)
    db.add_to_database(device, DatabaseType.devices_db)
    return device_id
