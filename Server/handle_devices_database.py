from pydantic import BaseModel
import json
import os

import consts


class NewDevice(BaseModel):
    stam: int  #TODO: remove


class Device(NewDevice):
    device_id: int


def init_devices_database():
    os.mkdir(consts.DEVICES_DATABASE_DIRECTORY)


def delete_devices_database():
    os.remove(consts.DEVICES_DATABASE_NAME)

# def create_devices_database_directory():
#     os.mkdir('/devices')


async def register_device(new_device: NewDevice):

    with open(consts.DEVICES_DATABASE_NAME, 'a') as database:

        device = Device(**new_device.dict(), device_id=consts.NUM_OF_DEVICES)
        json.dump(device, database)
        consts.NUM_OF_DEVICES += 1

    return device


async def get_device_database():
    with open('/devices/database.json', 'r') as database:
        result = database.read()

    return result
