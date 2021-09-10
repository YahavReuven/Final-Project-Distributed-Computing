
from dataclasses import dataclass

@dataclass
class NewProject:
    creator_id: str
    task_size: int
    base64_serialized_class: str
    base64_serialized_iterable: str
