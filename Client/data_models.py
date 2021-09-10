"""
Module used to define data classes.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Task:
    """ A class which holds information about the task for statistics."""
    pass


@dataclass
class ReceivedTask:
    project_id: str
    task_number: int
    task_size: int
    base64_serialized_class: str
    base64_serialized_iterable: str


# TODO: check if need to change to BaseModel
# TODO: maybe change results to not optional
@dataclass
class ReturnedTask:
    worker_id: str
    project_id: str
    task_number: int
    results: dict
    base64_zipped_additional_results: Optional[str] = None
    stop_called: bool = False
    is_exhausted: bool = False

