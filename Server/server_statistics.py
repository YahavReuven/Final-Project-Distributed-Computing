from datetime import datetime

from db import DBHandler
from consts import DatabaseType
from data_models import ProjectStatisticsServer

# TODO: handle errors, project does not exists


def create_project_statistics(project_id: str):
    database = DBHandler()
    tasks_statistics = []
    for project in database.get_database(DatabaseType.waiting_to_return_projects_db)[0]:
        if project.project_id == project_id:
            for task in project.tasks:
                for worker in task.workers:
                    tasks_statistics.append(worker.statistics)
            overall_project_time = project.finish_time - project.upload_time
            break

    statistics = ProjectStatisticsServer(task_statistics=tasks_statistics,
                                         overall_project_time=overall_project_time)
    return statistics