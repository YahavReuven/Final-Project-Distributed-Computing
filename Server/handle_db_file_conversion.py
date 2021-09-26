
from dataclasses import asdict
from datetime import datetime
from typing import Union

from data_models import (Device, DeviceDB, Project, Task, Worker, ProjectStorage,
                         DB, DevicesDB, ProjectsDB, WorkerDB, TaskDB, ProjectDB,
                         EncodedProjectsDB, EncodedDevicesDB)
import consts





def devices_db_to_encoded_devices_db(devices_db: DevicesDB, *, dict_form=False)\
        -> Union[EncodedDevicesDB, dict]:
    devices = []
    for device in devices_db.devices:
        devices.append(device_to_device_db(device))
    encoded_devices_db = EncodedDevicesDB(devices=devices)
    if dict_form:
        return asdict(encoded_devices_db)
    return encoded_devices_db


def device_to_device_db(device: Device, *, dict_form=False) -> Union[DeviceDB, dict]:
    """
    Converts a Device object to a DeviceDB object.

    Args:
        device (Device): a device.
        dict_form (bool) = True: whether or not to return a dict.
            In case of False a DeviceDB object is returned.

    Returns:
        DeviceDB: the device's database representation.

    """
    device_id = device.device_id
    # TODO: maybe add sort
    projects_ids = [project.project_id for project in device.projects]
    device_db = DeviceDB(device_id=device_id, projects_ids=projects_ids)
    if dict_form:
        return asdict(device_db)
    return device_db


def projects_db_to_encoded_projects_db(projects_db: ProjectsDB, *, dict_form=False)\
        -> Union[EncodedProjectsDB, dict]:
    active = []
    waiting = []
    finished = []
    for project in projects_db.active_projects:
        active.append(project_to_project_db(project))
    for project in projects_db.waiting_projects:
        waiting.append(project_to_project_db(project))
    for project in projects_db.finished_projects:
        finished.append(project_to_project_db(project))
    encoded_projects_db = EncodedProjectsDB(active_projects=active,
                                            waiting_projects=waiting,
                                            finished_projects=finished)
    if dict_form:
        return asdict(encoded_projects_db)
    return encoded_projects_db


def project_to_project_db(project: Project, *, dict_form=False) -> Union[ProjectDB, dict]:
    tasks = []
    for task in project.tasks:
        tasks.append(task_to_task_db(task))
    project_db = ProjectDB(project_id=project.project_id, tasks=tasks,
                           stop_number=project.stop_number,
                           stop_immediately=project.stop_immediately)
    if dict_form:
        return asdict(project_db)
    return project_db


def task_to_task_db(task: Task, *, dict_form=False) -> Union[TaskDB, dict]:
    workers = []
    for worker in task.workers:
        workers.append(worker_to_worker_db(worker))
    task_db = TaskDB(workers=workers)
    if dict_form:
        return asdict(task_db)
    return task_db


def worker_to_worker_db(worker: Worker, *, dict_form=False) -> Union[WorkerDB, dict]:
    sent_date_str = datetime_to_str(worker.sent_date)
    worker_db = WorkerDB(worker_id=worker.worker_id, sent_date=sent_date_str,
                         is_finished=worker.is_finished)
    if dict_form:
        return asdict(worker_db)
    return worker_db


def datetime_to_str(datetime_: datetime) -> str:
    return datetime_.strftime(consts.DATETIME_FORMAT)







def encoded_projects_db_to_projects_db(encoded_projects_db: Union[EncodedProjectsDB, dict], *, from_dict=False) -> ProjectsDB:
    if from_dict:
        encoded_projects_db = EncodedProjectsDB(**encoded_projects_db)
    active = []
    waiting = []
    finished = []
    for project in encoded_projects_db.active_projects:
        active.append(project_db_to_project(project))
    for project in encoded_projects_db.waiting_projects:
        waiting.append(project_db_to_project(project))
    for project in encoded_projects_db.finished_projects:
        finished.append(project_db_to_project(project))
    projects_db = ProjectsDB(active_projects=active, waiting_projects=waiting,
                             finished_projects=finished)
    return projects_db


def project_db_to_project(project_db: Union[ProjectDB, dict], *, from_dict=False) -> Project:
    if from_dict:
        project_db = ProjectDB(**project_db)
    tasks = []
    for task in project_db.tasks:
        tasks.append(task_db_to_task(task))
    project = Project(project_id=project_db.project_id, tasks=tasks,
                      stop_number=project_db.stop_number,
                      stop_immediately=project_db.stop_immediately)
    return project

def task_db_to_task(task_db: Union[TaskDB, dict], *, from_dict=False) -> Task:
    if from_dict:
        task_db = TaskDB(**task_db)
    workers = []
    for worker in task_db.workers:
        workers.append(worker_db_to_worker(worker))
    task = Task(workers=workers)
    return task


def worker_db_to_worker(worker_db: Union[WorkerDB, dict], *, from_dict=False) -> Worker:
    if from_dict:
        worker_db = WorkerDB(**worker_db)
    sent_date = str_to_date_time(worker_db.sent_date)
    worker = Worker(worker_id=worker_db.worker_id, sent_date=sent_date,
                    is_finished=worker_db.is_finished)
    return worker


def str_to_date_time(str_datetime: str) -> datetime:
    return datetime.strptime(str_datetime, consts.DATETIME_FORMAT)