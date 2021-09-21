from data_models import (Device, DeviceDB, Project, Task, Worker, ProjectStorage,
                         DB, DevicesDB, ProjectsDB, WorkerDB, TaskDB, ProjectDB)
import consts


def encode_projects_db(projects_db: ProjectsDB):

    for project in projects_db.active_projects

def encode_project(project: Project) -> ProjectDB:
    tasks_db = []
    for task in project.tasks:
        workers_db = []
        for worker in task.workers:
            workers_db.append(encode_worker(worker))
        tasks_db.append(encode_task(task, workers_db))
    project_db = ProjectDB(project_id=project.project_id, tasks=tasks_db,
                           stop_number=project.stop_number,
                           stop_immediately=project.stop_immediately)
    return project_db


def encode_task(task: Task, workers_db: list[WorkerDB]):
    return TaskDB(workers=workers_db)

def encode_worker(worker: Worker) -> WorkerDB:
    sent_date_str = worker.sent_date.strftime(consts.DATETIME_FORMAT)
    return WorkerDB(worker_id=worker.worker_id, sent_date_str=sent_date_str,
                               is_finished=worker.is_finished)