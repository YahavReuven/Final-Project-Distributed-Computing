from dataclasses import dataclass, field

DEVICES_DATABASE_DIRECTORY = './devices'
DEVICES_DATABASE_NAME = DEVICES_DATABASE_DIRECTORY + '/devices_database.json'
DEVICES_DATABASE_KEY = 'devices'

PROJECTS_DIRECTORY = './projects'
PROJECTS_DATABASE_NAME = PROJECTS_DIRECTORY + '/projects_database.json'
PROJECTS_DATABASE_KEY = 'projects'

PROJECT_STORAGE_PROJECT = '/project'
PROJECT_STORAGE_RESULTS = '/results'

PROJECT_STORAGE_ZIPPED_PROJECT_NAME_AND_TYPE = '/zipped_project.zip'

UPDATE_DB_DELAY = 60*0.1


@dataclass
class Iteration:
    iteration_number: int
    return_value: object


@dataclass
class Project:
    project_id: str
    iterations: list[Iteration] = field(default_factory=list)


# TODO: maybe add DeviceInfo that Device and DeviceDB will inherit from

@dataclass
class Device:
    device_id: str
    projects: list[Project] = field(default_factory=list)


@dataclass
class DeviceDB:
    device_id: str
    projects_ids: list[str] = field(default_factory=list)



