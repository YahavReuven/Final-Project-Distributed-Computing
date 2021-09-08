
from dataclasses import dataclass
from typing import Optional


@dataclass
class Task:
    project_id: str
    task_number: int
    task_size: int
    base64_serialized_class: str
    base64_serialized_iterable: str


# check if need to change to BaseModel
# TODO: maybe change results to not optional
@dataclass
class ReturnedTask:
    worker_id: str
    project_id: str
    task_number: int
    results: Optional[dict]
    base64_zipped_additional_results: Optional[str]
    stop_called: bool = False
    is_exhausted: bool = False

