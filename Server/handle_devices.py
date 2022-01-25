"""
Module used to handle devices.
"""
from uuid import uuid4

from consts import DatabaseType
from data_models import Device, DevicePermissions
from database import DBHandler, DBUtils
from authentication import authenticate_device
from errors import DeviceIsBlocked


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


async def block_device(device_id: str):
    """
    Blocks a device.

    Args:
        device_id (str): the id of the device to block.

    """
    authenticate_device(device_id)
    device = DBUtils.find_in_db(device_id, DatabaseType.devices_db)
    device.is_blocked = True


async def unblock_device(device_id: str):
    """
    Un-blocks a device.

    Args:
        device_id (str): the id of the device to unblock.

    """
    try:
        authenticate_device(device_id)
    except DeviceIsBlocked:
        device = DBUtils.find_in_db(device_id, DatabaseType.devices_db)
        device.is_blocked = False


async def get_devices_permissions() -> list[DevicePermissions]:
    """
    Returns the devices permissions.

    Returns:
        list[DevicePermissions]: the devices permissions.

    """
    db = DBHandler()

    devices = db.get_database(DatabaseType.devices_db)[0]
    permissions = []

    for device in devices:
        device_permission = DevicePermissions(device_id=device.device_id,
                                              is_blocked=device.is_blocked)
        permissions.append(device_permission)
    return permissions
