from data_models import ProjectStatisticsServer
import consts
from utils import create_path_string

import json

def save_statistics(statistics: dict):
    path = create_path_string(consts.STATISTICS_FILE + consts.JSON_EXTENSION)

    with open(path, "w") as file:
        json.dump(statistics, file)