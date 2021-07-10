"""
Module used
"""

import os

import consts
import handle_devices


def init_server():
    init_devices_database()
    handle_devices.devices_db_init()


def init_devices_database():
    """
    Initializes devices database and creates needed directories.
    """

    os.makedirs(consts.DEVICES_DATABASE_DIRECTORY, exist_ok=True)

    if not os.path.isfile(consts.DEVICES_DATABASE_NAME):
        with open(consts.DEVICES_DATABASE_NAME, 'w') as database:
            database.write('{ "' + consts.DEVICES_DATABASE_KEY + '" : [] }')
