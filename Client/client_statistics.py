from handle_users_data import UsersDataHandler
from data_models import StorageTaskStatistics, TaskStatistics
from datetime import datetime, timedelta
from dataclasses import asdict

# TODO: maybe return NONE
def get_task_statistics(user: UsersDataHandler, project_id: str, task_number: int) -> StorageTaskStatistics:
    for task in user.user.tasks:
        if(project_id == task.project_id and task_number == task.task_number):
            return task

def task_statistics_as_dict(statistics: TaskStatistics):
    result = asdict(statistics)
    for key, value in result.items():
        result[key] = str(value)
    return result
