from dataclasses import dataclass, field


@dataclass
class NewProject:
    creator_id: str
    task_size: int
    base64_serialized_class: str
    base64_serialized_iterable: str


@dataclass
class User:
    ip: str
    port: str
    device_id: str
    projects: field(default_factory=list)
    tasks: field(default_factory=list)


# TODO: check annotation for dict
@dataclass
class ReturnedProject:
    results: dict
    base64_zipped_additional_results: str