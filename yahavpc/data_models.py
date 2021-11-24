from dataclasses import dataclass, field
from datetime import timedelta

@dataclass
class TaskStatistics:
    pure_run_time: timedelta
    total_execution_time: timedelta

@dataclass
class TaskStatisticsServer:
    task_statistics: TaskStatistics
    with_communications: timedelta

@dataclass
class ProjectStatisticsServer:
    overall_project_time: timedelta
    task_statistics: list[TaskStatisticsServer] = field(default_factory=list)


@dataclass
class NewProject:
    creator_id: str
    task_size: int
    base64_serialized_class: str
    base64_serialized_iterable: str
    modules: list


@dataclass
class User:
    ip: str
    port: str
    device_id: str
    projects: list[ProjectStatisticsServer] = field(default_factory=list)
    tasks: list[TaskStatistics] = field(default_factory=list)




# TODO: check annotation for dict
@dataclass
class ReturnedProject:
    results: dict
    base64_zipped_additional_results: str
    statistics: dict
