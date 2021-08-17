import threading

import uvicorn
from fastapi import FastAPI

from handle_devices import register_device
from handle_projects import create_new_project, return_project_results
from handle_tasks import get_new_task, return_task_results
from db import DBHandler
from initialize_server import init_server, update_db
from data_models import SentTask, ReturnedProject
from errors import ServerError,  handle_server_error

app = FastAPI()

register_device = app.get('/register_device')(register_device)

create_new_project = app.post('/upload_new_project')(create_new_project)

# return_project_results = app.get('/get_project_results', response_model=ReturnedProject)(return_project_results)

get_new_task = app.get('/get_new_task', response_model=SentTask)(get_new_task)

return_task_results = app.post('/upload_task_results')(return_task_results)

app.exception_handler(ServerError)(handle_server_error)


if __name__ == '__main__':
    init_server()
    db = DBHandler()
    th = threading.Thread(target=update_db, args=(db,))
    th.start()
    uvicorn.run(app, host='0.0.0.0', port=8000)
