from dataclasses import dataclass, field

DEVICES_DATABASE_DIRECTORY = './devices'
DEVICES_DATABASE_NAME = DEVICES_DATABASE_DIRECTORY + '/devices_database.json'

PROJECTS_DATABASE_DIRECTORY = './projects'
PROJECTS_DATABASE_NAME = PROJECTS_DATABASE_DIRECTORY + '/projects_database.json'
UPDATE_DB_DELAY = 60*0.1


@dataclass
class Client:
    id: str
    is_active: bool
    projects: list[str] = field(default_factory=list)
