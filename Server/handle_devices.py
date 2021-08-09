"""
Module used to handle devices
"""

import json
import os
from uuid import UUID, uuid4

from pydantic import BaseModel

import consts
from consts import DatabaseType
from data_models import Device
from db_handler import DBHandler

# db = None
#
# def devices_db_init():
#     global db
#     db = DBHandler()



class DeviceInfo(BaseModel):
    stam: int  #TODO: remove


# class Device(DeviceInfo):
#     device_id: str
#
#
# class DeviceDBInfo(DeviceInfo):
#     is_active: bool


# # TODO: remove. only for testing
# def init_devices_database():
#     if not os.path.isdir(consts.DEVICES_DATABASE_DIRECTORY):
#         os.mkdir(consts.DEVICES_DATABASE_DIRECTORY)
#         with open(consts.DEVICES_DATABASE_NAME, 'w') as database:
#             database.write('{}')


# # TODO: remove. only for testing
# def delete_devices_database():
#     with open(consts.DEVICES_DATABASE_NAME, 'w') as database:
#         database.write('{}')


# TODO: maybe change return value to device id
async def register_device() -> str:  # device_info: DeviceInfo
    """

    Note:
        Assumes that './devices/devices_database.json' exists and contains '{}'
        or other devices.

    Args:
        device_info: information about the device

    Returns:

    """
    db = DBHandler()

    device_id = uuid4().hex
    device = Device(device_id=device_id)
    db.add_to_database(device, DatabaseType.devices_db)
    #db.devices_db[consts.DEVICES_DATABASE_KEY].append(device)

    # new_device = {device_id.hex: device_info.dict()}
    # data.update(new_device)

    return device_id


# TODO: remove. only for testing
async def get_device_database():
    with open(consts.DEVICES_DATABASE_NAME, 'r') as database:
        result = database.read()

    return result
