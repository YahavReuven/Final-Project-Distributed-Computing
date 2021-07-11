import threading

import uvicorn
from fastapi import FastAPI

from handle_devices import (register_device) #, Device, get_device_database,
                                     # delete_devices_database, init_devices_database,
                                     # delete_devices_database)
# from handle_projects_database import create_new_project
import consts
from db_handler import DBHandler
from initialize_server import init_server, update_db


app = FastAPI()


register_device = app.post('/register_device')(register_device)
# get_device_database = app.get('/devices')(get_device_database)
# delete_devices_database = app.get('/delete')(delete_devices_database)


# create_new_project = app.post('/new_project')(create_new_project)



if __name__ == '__main__':
    init_server()
    db = DBHandler()
    th = threading.Thread(target=update_db, args=(db,))
    th.start()
    uvicorn.run(app, host='0.0.0.0', port=8000)
