"""
Module used to handle the statistics of a client.
"""
from dataclasses import asdict

from handle_users_data import UsersDataHandler
from data_models import StorageTaskStatistics, TaskStatistics


# TODO: maybe return NONE
def get_task_statistics(user: UsersDataHandler, project_id: str, task_number: int) \
        -> StorageTaskStatistics:
    """
    Gets the statistics of a task.

    Args:
        user (UsersDataHandler): the user which executed the task.
        project_id (str): the id of the project of the task.
        task_number (int): the number of the task.

    Returns:
        StorageTaskStatistics: the statistics of the task.

    """
    for task in user.user.tasks:
        if project_id == task.project_id and task_number == task.task_number:
            return task


def task_statistics_as_dict(statistics: TaskStatistics) -> dict:
    """
    Translates the statistics to a format which can be sent to the server.

    Args:
        statistics (TaskStatistics): the statistics.

    Returns:
        dict: the statistics in dict format.

    """
    result = asdict(statistics)
    for key, value in result.items():
        result[key] = str(value)
    return result
