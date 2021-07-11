from dataclasses import dataclass, field

DEVICES_DATABASE_DIRECTORY = './devices'
DEVICES_DATABASE_NAME = DEVICES_DATABASE_DIRECTORY + '/devices_database.json'
DEVICES_DATABASE_KEY = 'devices'

PROJECTS_DATABASE_DIRECTORY = './projects'
PROJECTS_DATABASE_NAME = PROJECTS_DATABASE_DIRECTORY + '/projects_database.json'
PROJECTS_DATABASE_KEY = 'projects'

UPDATE_DB_DELAY = 60*0.1


@dataclass
class Project:
    project_id: str
    tasks: list[str] = field(default_factory=list)  # TODO: change to list of Task


@dataclass
class Device:
    device_id: str
    projects: list[Project] = field(default_factory=list)


@dataclass
class DeviceDB:
    device_id: str
    projects_ids: list[str] = field(default_factory=list)



