"""
Module used to define data classes.
"""
from dataclasses import dataclass, field
from typing import Optional


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


# TODO: check if need to change to BaseModel
@dataclass
class ReturnedTask:
    """ A finished task sent to the server. """
    worker_id: str
    project_id: str
    task_number: int
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
    projects: Optional[list[object]] = field(default_factory=list)
    tasks: Optional[list[object]] = field(default_factory=list)
