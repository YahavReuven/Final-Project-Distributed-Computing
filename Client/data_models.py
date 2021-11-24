"""
Module used to define data classes.
"""
from dataclasses import dataclass, field
from typing import Optional
from datetime import timedelta

from pydantic import BaseModel

@dataclass
class TaskStatistics:
    pure_run_time: timedelta
    total_execution_time: timedelta


@dataclass
class StorageTaskStatistics:
    project_id: str
    task_number: int
    statistics: TaskStatistics

@dataclass
class TaskStatisticsServer:
    task_statistics: TaskStatistics
    with_communications: timedelta

@dataclass
class ProjectStatisticsServer:
    overall_project_time: timedelta
    task_statistics: list[TaskStatisticsServer] = field(default_factory=list)


@dataclass
class Task:
    """ A class which holds information about the task for statistics."""
    pass


@dataclass
class ReceivedTask:
    """ A task received from the server for execution. """
    project_id: str
    task_number: int
    task_size: int
    base64_serialized_class: str
    base64_serialized_iterable: str
    modules: list


# TODO: check if need to change to BaseModel
@dataclass
class ReturnedTask:
    """ A finished task sent to the server. """
    worker_id: str
    project_id: str
    task_number: int
    statistics: dict
    results: dict
    base64_zipped_additional_results: Optional[str] = None
    stop_called: bool = False
    is_exhausted: bool = False


# TODO: change annotations
@dataclass
class User:
    """ A User in the client side. """
    ip: str
    port: int
    device_id: str
    projects: list[ProjectStatisticsServer] = field(default_factory=list)
    tasks: list[StorageTaskStatistics] = field(default_factory=list)
