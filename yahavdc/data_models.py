"""
Module used to define data classes.
"""
from dataclasses import dataclass, field
from datetime import timedelta


@dataclass
class TaskStatistics:
    """The statistics generated by a worker from a single task execution."""
    pure_run_time: timedelta
    total_execution_time: timedelta


@dataclass
class TaskStatisticsServer:
    """The statistics of a task generated by the server."""
    task_statistics: TaskStatistics
    with_communications: timedelta


@dataclass
class ProjectStatisticsServer:
    """The statistics of a project."""
    overall_project_time: timedelta
    task_statistics: list[TaskStatisticsServer] = field(default_factory=list)


@dataclass
class NewProject:
    """A new project to send to the server."""
    creator_id: str
    task_size: int
    parallel_func: str
    stop_func: str
    only_if_func: str
    base64_serialized_class: str
    base64_serialized_iterable: str
    modules: list


@dataclass
class User:
    """A user in the client side."""
    ip: str
    port: str
    device_id: str
    projects: list[ProjectStatisticsServer] = field(default_factory=list)
    tasks: list[TaskStatistics] = field(default_factory=list)


# TODO: check annotation for dict
@dataclass
class ReturnedProject:
    """The data of a finished project."""
    results: dict
    base64_zipped_additional_results: str
    statistics: str  # of json
.