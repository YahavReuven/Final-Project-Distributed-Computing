"""
Module used to define data classes and fastapi base models
"""
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional, Union

from pydantic import BaseModel


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


class NewProject(BaseModel):
    """A new project sent from the client."""
    creator_id: str
    task_size: int
    parallel_func: str
    stop_func: str
    only_if_func: str
    base64_serialized_class: str
    base64_serialized_iterable: str
    modules: list  # Should be empty if is not needed


class ReturnedProject(BaseModel):
    """A finished project's data."""
    results: dict
    base64_zipped_additional_results: str
    statistics: str  # of json


class SentTask(BaseModel):
    """A task sent to the client."""
    project_id: str
    task_number: int
    task_size: int
    base64_serialized_class: str
    base64_serialized_iterable: str
    modules: list
    parallel_func: str
    stop_func: str
    only_if_func: str


class ReturnedTask(BaseModel):
    """A returned task from a worker."""
    worker_id: str
    project_id: str
    task_number: int
    statistics: dict
    results: dict
    base64_zipped_additional_results: Optional[str] = None
    stop_called: bool = False
    is_exhausted: bool = False


class DevicePermissions(BaseModel):
    """The permissions of a device."""
    device_id: str
    is_blocked: bool


@dataclass
class Worker:
    """A worker which executes a task."""
    worker_id: str
    sent_date: datetime
    statistics: TaskStatisticsServer = None
    is_finished: bool = False


@dataclass
class Task:
    """A task's representation in the database."""
    workers: list[Worker] = field(default_factory=list)


@dataclass
class Project:
    """A project's representation in the database."""
    project_id: str
    upload_time: datetime
    finish_time: Union[None, datetime] = None
    tasks: list[Task] = field(default_factory=list)
    stop_number: int = -1
    stop_immediately: bool = False


@dataclass
class ProjectStorage:
    """The stored data of a project in a file."""
    base64_serialized_class: str
    base64_serialized_iterable: str
    modules: list
    task_size: int
    parallel_func: str
    stop_func: str
    only_if_func: str


@dataclass
class Device:
    """A device's representation in the memory database."""
    device_id: str
    projects: list[Project] = field(default_factory=list)
    is_blocked: bool = False


@dataclass
class DeviceDB:
    """A device's representation in the file database."""
    device_id: str
    projects_ids: list[str] = field(default_factory=list)
    is_blocked: bool = False


@dataclass
class DevicesDB:
    """The devices database."""
    devices: list[Device] = field(default_factory=list)


@dataclass
class EncodedDevicesDB:
    """The encoded devices database."""
    devices: list[DeviceDB] = field(default_factory=list)


@dataclass
class ProjectsDB:
    """The projects database."""
    active_projects: list[Project] = field(default_factory=list)
    waiting_projects: list[Project] = field(default_factory=list)
    finished_projects: list[Project] = field(default_factory=list)


@dataclass
class DB:
    """The database."""
    devices_db: DevicesDB = DevicesDB()
    projects_db: ProjectsDB = ProjectsDB()
