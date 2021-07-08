import json
import os
from uuid import UUID, uuid4

from pydantic import BaseModel

import consts


class DeviceInfo(BaseModel):
    stam: int  #TODO: remove


class Device(DeviceInfo):
    device_id: UUID


class DeviceDBInfo(DeviceInfo):
    is_active: bool


# TODO: remove. only for testing
def init_devices_database():
    if not os.path.isdir(consts.DEVICES_DATABASE_DIRECTORY):
        os.mkdir(consts.DEVICES_DATABASE_DIRECTORY)
        with open(consts.DEVICES_DATABASE_NAME, 'w') as database:
            database.write('{}')


# TODO: remove. only for testing
def delete_devices_database():
    with open(consts.DEVICES_DATABASE_NAME, 'w') as database:
        database.write('{}')


# TODO: maybe change return value to device id
async def register_device(device_info: DeviceInfo) -> Device:
    """

    Note:
        Assumes that './devices/devices_database.json' exists and contains '{}'
        or other devices.

    Args:
        device_info: information about the device

    Returns:

    """
    with open(consts.DEVICES_DATABASE_NAME, 'r') as database:
        data = json.load(database)

    device_id = uuid4()
    device = Device(**device_info.dict(), device_id=device_id)
    new_device = {device_id.hex: device_info.dict()}
    data.update(new_device)

    with open(consts.DEVICES_DATABASE_NAME, 'w') as database:
        json.dump(data, database)

    return device


async def get_device_database():
    with open(consts.DEVICES_DATABASE_NAME, 'r') as database:
        result = database.read()

    return result
