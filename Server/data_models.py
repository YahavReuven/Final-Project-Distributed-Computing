"""
Module used to define data classes and fastapi base models
"""

from dataclasses import dataclass, field
from datetime import datetime
from pydantic import BaseModel


class NewProject(BaseModel):
    """A new project sent from the client"""
    creator_id: str  # TODO: the device id of the creator of the project. maybe change to user
    task_size: int
    base64_serialized_class: str
    base64_serialized_iterable: str


class SentTask(BaseModel):
    """A task sent to the client"""
    project_id: str
    task_number: int
    base64_serialized_class: str
    base64_serialized_iterable: str


class ReturnedTask(BaseModel):
    worker_id: str
    project_id: str
    task_number: int
    base64_zipped_results: str
    stop_called: bool = False
    is_exhausted: bool = False


@dataclass
class Worker:
    worker_id: str
    sent_date: datetime
    is_finished: bool = False


@dataclass
class Task:
    workers: list[Worker] = field(default_factory=list)


# @dataclass
# class TaskDB:
#     workers_ids: list[str] = field(default_factory=list)


@dataclass
class Project:
    project_id: str
    tasks: list[Task] = field(default_factory=list)
    stop_number: int = -1
    stop_immediately: bool = False


# TODO: maybe add DeviceInfo that Device and DeviceDB will inherit from

@dataclass
class Device:
    """A device's representation in the memory database"""
    device_id: str
    projects: list[Project] = field(default_factory=list)


@dataclass
class DeviceDB:
    """A device's representation in the file database"""
    device_id: str
    projects_ids: list[str] = field(default_factory=list)


