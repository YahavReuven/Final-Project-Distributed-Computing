import uvicorn
from fastapi import FastAPI

from handle_devices_database import register_device, Device, get_device_database, delete_devices_database, init_devices_database, delete_devices_database

from handle_tasks_database import create_new_project

app = FastAPI()

#init_devices_database()

register_device = app.post("/register_device", response_model=Device)(register_device)
get_device_database = app.get('/devices')(get_device_database)
delete_devices_database = app.get('/delete')(delete_devices_database)


create_new_project = app.post('/new_project')(create_new_project)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)