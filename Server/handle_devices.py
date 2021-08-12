"""
Module used to handle devices
"""
"""passed check"""

from uuid import uuid4

from consts import DatabaseType
from data_models import Device
from db_handler import DBHandler


# TODO: maybe change return value to device id
async def register_device() -> str:  # device_info: DeviceInfo
    """

    Note:
        Assumes that './devices/devices_database.json' exists and contains '{}'
        or other devices.

    Returns:
        str: the device id.

    """
    db = DBHandler()

    device_id = uuid4().hex
    device = Device(device_id=device_id)
    db.add_to_database(device, DatabaseType.devices_db)
    return device_id
