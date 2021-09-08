
from dataclasses import dataclass


@dataclass
class Task:
    project_id: str
    task_number: int
    base64_serialized_class: str
    base64_serialized_iterable: str

