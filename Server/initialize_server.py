"""
Module used to initialize the server and update
"""
import time
import os

import consts
import handle_devices
from db_handler import DBHandler


def update_db(db: DBHandler):
    while True:
        time.sleep(consts.UPDATE_DB_DELAY)
        db.update_db()


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
